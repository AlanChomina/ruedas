-- =============================================================================
-- Ruedas · Datos de prueba FICTICIOS (no son personas ni carros reales)
--
-- Requisitos antes de ejecutar:
--   1. Ya ejecutaste supabase/migraciones/001_esquema_inicial.sql
--   2. Creaste en Supabase (sección de autenticación/usuarios) un usuario de
--      prueba con el correo:  agencia.prueba@example.com
--      (example.com es un dominio reservado para ejemplos; nadie lo usa).
--
-- Dónde ejecutar: editor de SQL de tu proyecto de Supabase.
-- Se puede ejecutar más de una vez: borra y vuelve a crear SOLO estos datos.
-- =============================================================================
do $$
declare
  usuario_id uuid;
  agencia1 uuid;
  agencia2 uuid;
begin
  select id into usuario_id from auth.users where email = 'agencia.prueba@example.com';
  if usuario_id is null then
    raise exception 'Primero crea en Supabase el usuario agencia.prueba@example.com';
  end if;

  -- Limpia datos de prueba anteriores de este usuario
  delete from public.carros where responsable_id = usuario_id;
  delete from public.agencias where responsable_id = usuario_id;

  update public.perfiles
     set nombre_publico = 'Agencia de prueba', tipo_cuenta = 'agencia'
   where id = usuario_id;

  insert into public.agencias (responsable_id, nombre, descripcion, zona, estado_verificacion, verificado_en)
  values (usuario_id, 'Autos Otay Seminuevos (prueba)',
          'Compra, venta y consignación de seminuevos revisados mecánicamente.', 'Otay', 'verificado', now())
  returning id into agencia1;

  insert into public.agencias (responsable_id, nombre, descripcion, zona)
  values (usuario_id, 'Lote La Mesa Motors (prueba)',
          'Lote familiar dedicado a compactos y carros económicos.', 'La Mesa')
  returning id into agencia2;

  insert into public.agencias_ubicacion (agencia_id, direccion)
  values (agencia1, 'Dirección ficticia de prueba, Tijuana');

  insert into public.carros
    (responsable_id, agencia_id, nombre, carroceria, version, kilometraje, tamano, transmision, combustible,
     detalles, acepta_cambio, acepta_credito, precio_negociable, servicios_al_dia, unico_dueno, zona, estado)
  values
    (usuario_id, agencia1, 'Toyota Camry 2019', 'sedán', 'LE Híbrido', 68000, 'mediano', 'automática', 'híbrido',
     'Muy cuidado, cómodo en carretera y rinde muchísimo en ciudad.', true, true, null, true, true, 'Playas de Tijuana', 'disponible'),
    (usuario_id, agencia1, 'Suzuki Jimny 2021', 'camioneta', 'GLX 4x4', 24000, 'compacto', 'manual', 'gasolina',
     'Ágil y divertida. Ideal para la ciudad y para salir a la terracería.', true, null, true, true, true, 'Zona Río', 'disponible'),
    (usuario_id, agencia1, 'Volkswagen Passat 2013', 'sedán', 'TDI', 182000, 'grande', 'manual', 'diésel',
     'Noble y rendidor. Su dueño se muda de ciudad y necesita venderlo pronto.', true, true, false, true, false, 'Otay', 'urgente'),
    (usuario_id, agencia1, 'Honda HR-V 2020', 'camioneta', 'No especificada', 41000, 'compacto', 'automática', 'gasolina',
     'Discreta por fuera, muy amplia por dentro. Ya tiene un trato en curso.', null, null, true, true, true, 'La Mesa', 'en_proceso'),
    (usuario_id, agencia1, 'Nissan Versa 2018', 'sedán', 'Sense', 88000, 'compacto', 'manual', 'gasolina',
     'Económico y confiable. Está en el taller por cambio de clutch.', true, true, true, true, true, 'Cacho', 'en_taller'),
    (usuario_id, null, 'Nissan Kicks 2019', 'camioneta', 'Advance', 57000, 'compacto', 'automática', 'gasolina',
     'Visto por última vez estacionado cerca de un parque de la colonia.', null, null, null, true, true, 'Cacho', 'robado'),
    (usuario_id, null, 'Sin identificar', 'sedán', 'No especificada', null, 'mediano', 'manual', 'gasolina',
     'Recuperado sin placas, con un golpe en la defensa trasera. Está resguardado.', null, null, null, false, false, 'Playas de Tijuana', 'recuperado');

  raise notice 'Datos de prueba creados: 2 agencias y 7 carros.';
end $$;
