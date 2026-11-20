-- SOLO PARA PRUEBAS LOCALES. Comprueba que la migración 001 protege los datos.
-- Cada prueba imprime "OK: ..." o detiene todo con "FALLÓ: ...".
\set ON_ERROR_STOP 1
set client_min_messages = notice;

-- ---------------------------------------------------------------------------
-- Ayudantes de prueba
-- ---------------------------------------------------------------------------
create schema pruebas;
grant usage on schema pruebas to anon, authenticated;

create function pruebas.afirmar(condicion boolean, mensaje text) returns void language plpgsql as $$
begin
  if condicion is not true then raise exception 'FALLÓ: %', mensaje; end if;
  raise notice 'OK: %', mensaje;
end $$;

-- Ejecuta SQL que DEBE ser rechazado con un error.
create function pruebas.debe_fallar(consulta text, mensaje text) returns void language plpgsql as $$
begin
  execute consulta;
  raise exception 'FALLÓ (se permitió): %', mensaje;
exception
  when insufficient_privilege or check_violation or not_null_violation
       or invalid_text_representation or foreign_key_violation or unique_violation then
    raise notice 'OK: % [%]', mensaje, sqlerrm;
end $$;

-- Ejecuta SQL y devuelve cuántas filas cambió.
create function pruebas.filas(consulta text) returns int language plpgsql as $$
declare n int;
begin
  execute consulta; get diagnostics n = row_count; return n;
end $$;
grant execute on all functions in schema pruebas to anon, authenticated;

-- ---------------------------------------------------------------------------
-- Usuarios ficticios (nunca datos reales)
-- ---------------------------------------------------------------------------
insert into auth.users (id, email, raw_user_meta_data) values
 ('00000000-0000-0000-0000-00000000000a', 'ana@ejemplo.test',
   '{"nombre_publico":"Ana Prueba","tipo_cuenta":"comprador","nivel_verificacion":"habilitada"}'),
 ('00000000-0000-0000-0000-00000000000b', 'beto@ejemplo.test',
   '{"nombre_publico":"Agencia Prueba","tipo_cuenta":"agencia"}'),
 ('00000000-0000-0000-0000-00000000000c', 'caro@ejemplo.test',
   '{"nombre_publico":"Caro Vendedor","tipo_cuenta":"vendedor"}'),
 ('00000000-0000-0000-0000-00000000000d', 'admin@ejemplo.test',
   '{"nombre_publico":"Admin Prueba","tipo_cuenta":"administrador"}'),
 ('00000000-0000-0000-0000-00000000000e', 'x@ejemplo.test', '{}');

\echo '== Registro automático de perfiles'
select pruebas.afirmar((select count(*) = 5 from public.perfiles), 'cada usuario nuevo recibe un perfil');
select pruebas.afirmar((select count(*) = 5 from public.perfiles_privados), 'cada usuario nuevo recibe datos privados');
select pruebas.afirmar((select nivel_verificacion = 'registrada' from public.perfiles
  where id = '00000000-0000-0000-0000-00000000000a'), 'el registro ignora un nivel de verificación enviado por el usuario');
select pruebas.afirmar((select tipo_cuenta = 'comprador' from public.perfiles
  where id = '00000000-0000-0000-0000-00000000000d'), 'un tipo de cuenta inválido ("administrador") se convierte en comprador');
select pruebas.afirmar((select nombre_publico = 'Usuario de Ruedas' from public.perfiles
  where id = '00000000-0000-0000-0000-00000000000e'), 'sin nombre se asigna uno genérico');

-- Preparación como administrador del sistema (equivale al editor SQL de Supabase)
insert into public.administradores (usuario_id) values ('00000000-0000-0000-0000-00000000000d');
update public.perfiles set nivel_verificacion = 'habilitada' where id = '00000000-0000-0000-0000-00000000000c';
insert into public.agencias (id, responsable_id, nombre, estado_verificacion) values
 ('10000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-00000000000b', 'Agencia Verificada Prueba', 'verificado'),
 ('10000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-00000000000b', 'Agencia Rechazado Prueba', 'rechazado');
insert into public.agencias_ubicacion (agencia_id, direccion) values
 ('10000000-0000-0000-0000-000000000001', 'Calle Ficticia 123, Tijuana');
insert into public.carros (id, responsable_id, agencia_id, nombre, carroceria, tamano, zona, oculto) values
 ('20000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-00000000000b', '10000000-0000-0000-0000-000000000001', 'Visible', 'sedán', 'mediano', 'Otay', false),
 ('20000000-0000-0000-0000-000000000002', '00000000-0000-0000-0000-00000000000b', '10000000-0000-0000-0000-000000000001', 'Oculto', 'camioneta', 'compacto', 'Otay', true);
insert into public.carros_fotos (carro_id, ruta_archivo) values
 ('20000000-0000-0000-0000-000000000001', 'carros/visible.jpg'),
 ('20000000-0000-0000-0000-000000000002', 'carros/oculto.jpg');

-- ---------------------------------------------------------------------------
\echo '== Visitante sin sesión (anon)'
begin;
set local role anon;
select pruebas.afirmar((select count(*) = 5 from public.perfiles), 've perfiles públicos');
select pruebas.afirmar((select count(*) = 1 from public.carros), 've solo carros no ocultos');
select pruebas.afirmar((select count(*) = 1 from public.carros_fotos), 'no ve fotos de carros ocultos');
select pruebas.afirmar((select count(*) = 1 from public.agencias), 'no ve agencias rechazados');
select pruebas.debe_fallar('select * from public.perfiles_privados', 'no puede leer datos privados');
select pruebas.debe_fallar('select * from public.agencias_ubicacion', 'no puede leer direcciones de agencias');
select pruebas.debe_fallar('select * from public.administradores', 'no puede leer la lista de administradores');
select pruebas.debe_fallar($$insert into public.carros (responsable_id, nombre, carroceria, tamano, zona)
  values ('00000000-0000-0000-0000-00000000000b','X','sedán','grande','Otay')$$, 'no puede publicar carros');
rollback;

-- ---------------------------------------------------------------------------
\echo '== Ana: comprador recién registrada'
begin;
set local role authenticated;
set local request.jwt.claims = '{"sub":"00000000-0000-0000-0000-00000000000a"}';
select pruebas.afirmar(pruebas.filas($$update public.perfiles set biografia = 'Me encantan los carros'
  where id = '00000000-0000-0000-0000-00000000000a'$$) = 1, 'puede editar su propio perfil');
select pruebas.debe_fallar($$update public.perfiles set nivel_verificacion = 'habilitada'
  where id = '00000000-0000-0000-0000-00000000000a'$$, 'no puede subirse su nivel de verificación');
select pruebas.debe_fallar($$update public.perfiles set tipo_cuenta = 'agencia'
  where id = '00000000-0000-0000-0000-00000000000a'$$, 'no puede cambiar su tipo de cuenta');
select pruebas.afirmar(pruebas.filas($$update public.perfiles set biografia = 'hackeado'
  where id = '00000000-0000-0000-0000-00000000000b'$$) = 0, 'no puede editar el perfil de otra persona');
select pruebas.afirmar((select count(*) = 1 from public.perfiles_privados), 'solo ve sus propios datos privados');
select pruebas.debe_fallar($$update public.perfiles_privados set telefono_verificado = true
  where id = '00000000-0000-0000-0000-00000000000a'$$, 'no puede marcar su teléfono como verificado');
select pruebas.debe_fallar($$update public.perfiles_privados set telefono = 'no-es-telefono'
  where id = '00000000-0000-0000-0000-00000000000a'$$, 'rechaza un teléfono con formato inválido');
select pruebas.afirmar((select count(*) = 0 from public.agencias_ubicacion), 'no ve direcciones de agencias ajenos');
select pruebas.afirmar((select count(*) = 0 from public.carros_historial_estados), 'no ve historial de carros ajenos');
select pruebas.debe_fallar($$insert into public.agencias (responsable_id, nombre, estado_verificacion)
  values ('00000000-0000-0000-0000-00000000000a', 'Mi Agencia', 'verificado')$$, 'no puede registrar una agencia ya verificado');
select pruebas.afirmar(pruebas.filas($$insert into public.agencias (responsable_id, nombre)
  values ('00000000-0000-0000-0000-00000000000a', 'Agencia de Ana')$$) = 1, 'puede registrar una agencia');
select pruebas.afirmar((select estado_verificacion = 'pendiente' from public.agencias where nombre = 'Agencia de Ana'),
  'su agencia nuevo queda pendiente de verificación');
select pruebas.debe_fallar($$insert into public.agencias (responsable_id, nombre)
  values ('00000000-0000-0000-0000-00000000000b', 'Agencia a nombre de otro')$$, 'no puede registrar una agencia a nombre de otra persona');
select pruebas.debe_fallar($$insert into public.carros (responsable_id, nombre, carroceria, tamano, zona)
  values ('00000000-0000-0000-0000-00000000000a','Firulais','sedán','grande','Centro')$$, 'sin estar habilitada no puede publicar carros');
select pruebas.afirmar(pruebas.filas($$insert into public.favoritos (usuario_id, carro_id)
  values ('00000000-0000-0000-0000-00000000000a','20000000-0000-0000-0000-000000000001')$$) = 1, 'puede guardar un favorito');
select pruebas.debe_fallar($$insert into public.favoritos (usuario_id, carro_id)
  values ('00000000-0000-0000-0000-00000000000c','20000000-0000-0000-0000-000000000001')$$, 'no puede guardar favoritos a nombre de otra persona');
select pruebas.debe_fallar($$insert into public.favoritos (usuario_id, carro_id)
  values ('00000000-0000-0000-0000-00000000000a','20000000-0000-0000-0000-000000000002')$$, 'no puede guardar como favorito un carro oculto');
select pruebas.afirmar(pruebas.filas($$update public.carros set nombre = 'Robado'
  where id = '20000000-0000-0000-0000-000000000001'$$) = 0, 'no puede editar carros ajenos');
rollback;

-- ---------------------------------------------------------------------------
\echo '== Beto: responsable de una agencia verificada'
begin;
set local role authenticated;
set local request.jwt.claims = '{"sub":"00000000-0000-0000-0000-00000000000b"}';
select pruebas.afirmar((select count(*) = 2 from public.carros), 've sus carros, incluido el oculto');
select pruebas.afirmar((select count(*) = 2 from public.agencias), 've su agencia rechazado además del verificado');
select pruebas.afirmar((select count(*) = 1 from public.agencias_ubicacion), 've la dirección de su agencia');
select pruebas.afirmar(pruebas.filas($$insert into public.carros (responsable_id, agencia_id, nombre, carroceria, tamano, zona)
  values ('00000000-0000-0000-0000-00000000000b','10000000-0000-0000-0000-000000000001','Nuevo','sedán','grande','Otay')$$) = 1,
  'con agencia verificada puede publicar carros');
select pruebas.afirmar(pruebas.filas($$update public.carros set estado = 'en_proceso'
  where nombre = 'Nuevo'$$) = 1, 'puede cambiar el estado de su carro');
select pruebas.afirmar((select count(*) = 2 from public.carros_historial_estados
  where carro_id = (select id from public.carros where nombre = 'Nuevo')), 'el historial registra publicación y cambio de estado');
select pruebas.afirmar((select estado_anterior = 'disponible' and estado_nuevo = 'en_proceso'
  and cambiado_por = '00000000-0000-0000-0000-00000000000b'
  from public.carros_historial_estados where carro_id = (select id from public.carros where nombre = 'Nuevo')
  order by id desc limit 1), 'el historial guarda estado anterior, nuevo y quién lo cambió');
select pruebas.debe_fallar($$insert into public.carros_historial_estados (carro_id, estado_nuevo)
  select id, 'vendido' from public.carros where nombre = 'Nuevo'$$, 'no puede escribir el historial a mano');
select pruebas.debe_fallar($$update public.carros set oculto = false
  where id = '20000000-0000-0000-0000-000000000002'$$, 'no puede quitar la ocultación de moderación');
select pruebas.debe_fallar($$update public.agencias set estado_verificacion = 'verificado'
  where id = '10000000-0000-0000-0000-000000000002'$$, 'no puede aprobar su propia agencia');
select pruebas.debe_fallar($$insert into public.carros (responsable_id, agencia_id, nombre, carroceria, tamano, zona, oculto)
  values ('00000000-0000-0000-0000-00000000000b','10000000-0000-0000-0000-000000000001','X','sedán','grande','Otay', false)$$,
  'no puede fijar la columna de ocultación al publicar');
select pruebas.debe_fallar($$insert into public.carros (responsable_id, nombre, carroceria, tamano, zona)
  values ('00000000-0000-0000-0000-00000000000b','X','dragon','grande','Otay')$$, 'rechaza carrocerias no permitidas');
rollback;

-- ---------------------------------------------------------------------------
\echo '== Caro: vendedor habilitada sin agencia'
begin;
set local role authenticated;
set local request.jwt.claims = '{"sub":"00000000-0000-0000-0000-00000000000c"}';
select pruebas.afirmar(pruebas.filas($$insert into public.carros (responsable_id, nombre, carroceria, tamano, zona)
  values ('00000000-0000-0000-0000-00000000000c','Vocho 1998','camioneta','compacto','Centro')$$) = 1,
  'una persona habilitada puede publicar sin agencia');
select pruebas.debe_fallar($$insert into public.carros (responsable_id, agencia_id, nombre, carroceria, tamano, zona)
  values ('00000000-0000-0000-0000-00000000000c','10000000-0000-0000-0000-000000000001','X','camioneta','compacto','Centro')$$,
  'no puede publicar a nombre dla agencia de otra persona');
select pruebas.afirmar((select version = 'No especificada' from public.carros where nombre = 'Vocho 1998'),
  'la versión vacía queda como "No especificada"');
rollback;

-- ---------------------------------------------------------------------------
\echo '== Administradora'
begin;
set local role authenticated;
set local request.jwt.claims = '{"sub":"00000000-0000-0000-0000-00000000000d"}';
select pruebas.afirmar((select count(*) = 5 from public.perfiles_privados), 'puede leer datos privados para revisión');
select pruebas.afirmar((select count(*) = 1 from public.agencias_ubicacion), 'puede leer direcciones de agencias');
select pruebas.afirmar((select count(*) = 2 from public.carros), 've carros ocultos para moderarlos');
rollback;

-- ---------------------------------------------------------------------------
\echo '== Reglas automáticas'
update public.perfiles_privados set telefono = '6640000000', telefono_verificado = true
  where id = '00000000-0000-0000-0000-00000000000a';
begin;
set local role authenticated;
set local request.jwt.claims = '{"sub":"00000000-0000-0000-0000-00000000000a"}';
update public.perfiles_privados set telefono = '6641111111' where id = '00000000-0000-0000-0000-00000000000a';
select pruebas.afirmar((select not telefono_verificado from public.perfiles_privados),
  'cambiar el teléfono quita la verificación');
rollback;

\echo '== TODAS LAS PRUEBAS PASARON'
