create table if not exists users
(
    user_id         serial,
    user_name       text                     not null,
    user_password   text                     not null,
    user_permission text                     not null,
    user_type       integer,
    user_created_at timestamp without time zone not null,
    user_updated_at timestamp without time zone

);

create table if not exists teams
(
    team_id             serial,
    team_name           text not null,
    team_leader         text,
    team_sub_leader     text,
    team_login_id       text,
    team_login_password text
);

create table if not exists schedules
(
    schedule_id         serial,
    schedule_number     integer not null,
    schedule_name       text,
    schedule_type       integer not null,
    schedule_option     jsonb,
    schedule_started_at time,
    schedule_ended_at   time
);

create table if not exists scores
(
    score_id         serial,
    schedule_id      integer                  not null,
    team_id          integer                  not null,
    race_number      integer                  not null,
    race_gender      integer                  not null,
    score            integer                  not null,
    score_created_at timestamp without time zone not null,
    score_updated_at timestamp without time zone
);

create table if not exists options
(
    option_name  text    not null,
    option_value integer not null
);

create table if not exists entrys
(
    entry_id         serial                                                  not null,
    team_id          integer                                                 not null,
    schedule_id      integer                                                 not null,
    entry            jsonb                                                   not null,
    entry_created_at timestamp without time zone,
    entry_updated_at timestamp without time zone
);

create table if not exists list_of_name
(
    id      serial  not null,
    number  text    not null,
    name    text    not null,
    gender  text    not null,
    team_id integer not null
);

create table absence_report
(
    absence_id serial,
    primary_id integer not null
);