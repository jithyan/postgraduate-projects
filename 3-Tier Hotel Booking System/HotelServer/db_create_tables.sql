CREATE TABLE vacancy (
  date TEXT NOT NULL,
  vacant INTEGER NOT NULL,
  PRIMARY KEY(date)
);

CREATE TABLE booking (
  booking_id INTEGER PRIMARY KEY NOT NULL,
  guest_name TEXT NOT NULL,
  checkin_date TEXT NOT NULL,
  checkout_date TEXT NOT NULL,
  phone TEXT NOT NULL,
  email TEXT NOT NULL,
  credit_card TEXT NOT NULL
);
