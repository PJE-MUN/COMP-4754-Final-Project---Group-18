CREATE Database IF NOT EXISTS Hospital;
use Hospital;
CREATE ROLE if not exists doctor;
CREATE ROLE if not exists nurse;
CREATE ROLE if not exists patient;
grant all on Hospital.* to doctor;
grant all on Hospital.* to nurse;
grant SELECT on Hospital.appts to patient;
