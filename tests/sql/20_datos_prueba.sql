-- SOLO PARA PRUEBAS LOCALES: comprueba el archivo de datos ficticios.
\set ON_ERROR_STOP 1
insert into auth.users (email) values ('agencia.prueba@example.com');
\i supabase/datos_prueba/datos_ficticios.sql
\i supabase/datos_prueba/datos_ficticios.sql
begin;
set local role anon;
select pruebas.afirmar((select count(*) = 7 from public.carros a join public.perfiles p on p.id = a.responsable_id where p.nombre_publico = 'Agencia de prueba'), 'un visitante ve los 7 carros de prueba (sin duplicados)');
select pruebas.afirmar((select count(*) = 5 from public.carros a join public.perfiles p on p.id = a.responsable_id where p.nombre_publico = 'Agencia de prueba' and estado in ('disponible','urgente','en_proceso','en_consignacion','en_taller')), '5 carros en el catálogo de compra');
select pruebas.afirmar((select count(*) = 2 from public.agencias where nombre like '%(prueba)'), 'se ven los 2 agencias de prueba');
rollback;
\echo '== DATOS DE PRUEBA OK'

-- Alerta ficticia (requiere la migración 002)
\i supabase/datos_prueba/alerta_ficticia.sql
\i supabase/datos_prueba/alerta_ficticia.sql
begin;
set local role anon;
select pruebas.afirmar((select count(*) = 1 from public.alertas where nombre_carro = 'Nissan Tsuru (prueba)'),
  'la alerta ficticia se crea una sola vez aunque se ejecute dos veces');
select pruebas.afirmar((select latitud_aprox = 32.51 from public.alertas where nombre_carro = 'Nissan Tsuru (prueba)'),
  'la alerta ficticia tiene su punto aproximado');
rollback;
\echo '== ALERTA FICTICIA OK'
