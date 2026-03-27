-- Appointments table
CREATE TABLE hair2go_appointments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  date DATE NOT NULL,
  time_from TIME NOT NULL,
  time_to TIME NOT NULL,
  client_name TEXT NOT NULL,
  barber TEXT NOT NULL CHECK (barber IN ('Sonia', 'Pavlos')),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Optional: simple users table if you want to manage them in DB
CREATE TABLE hair2go_users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('admin', 'staff'))
);