drop table if exists advice;
create table advice (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);
