create table if not exists users_pay_plans
(
    id                    bigint auto_increment
        primary key,
    name                  varchar(32)                        not null,
    price                 int                                not null,
    max_image_count       bigint                             not null,
    max_image_size        bigint                             not null,
    max_image_group_count bigint                             not null,
    updated_at            datetime default CURRENT_TIMESTAMP null,
    created_at            datetime default CURRENT_TIMESTAMP null
);

create table if not exists users
(
    id         bigint auto_increment
        primary key,
    email      varchar(64)                           not null,
    pw         varchar(256)                          not null,
    payplan_id bigint                                not null,
    status     varchar(32) default 'ACTIVE'          null,
    is_admin   tinyint(1)  default 0                 null,
    updated_at datetime    default CURRENT_TIMESTAMP null,
    created_at datetime    default CURRENT_TIMESTAMP null,
    constraint users_pay_plans_id_fk
        foreign key (payplan_id) references users_pay_plans (id)
);

create table if not exists users_api_keys
(
    id         bigint auto_increment
        primary key,
    user_id    bigint                             not null,
    access_key varchar(64)                        not null,
    secret_key varchar(64)                        null,
    deleted_at datetime                           null,
    updated_at datetime default CURRENT_TIMESTAMP null,
    created_at datetime default CURRENT_TIMESTAMP null,
    constraint users_api_keys_users_id_fk
        foreign key (user_id) references users (id)
);

create table if not exists users_api_keys_whitelist
(
    id         bigint                             not null
        primary key,
    api_key_id bigint                             not null,
    ip         varchar(64)                        not null,
    updated_At datetime default CURRENT_TIMESTAMP not null,
    created_at datetime default CURRENT_TIMESTAMP not null,
    constraint users_api_keys_whitelist_FK
        foreign key (api_key_id) references users_api_keys (id)
);

create table if not exists images_groups
(
    id               bigint auto_increment primary key,
    uuid             varchar(64)                        not null,
    image_group_name varchar(64)                        not null,
    image_count      int      default 0                 null,
    updated_at       datetime default CURRENT_TIMESTAMP not null,
    created_at       datetime default CURRENT_TIMESTAMP not null
);

create table if not exists images
(
    id              bigint auto_increment
        primary key,
    image_group_id  bigint                             not null,
    uuid            varchar(64)                        not null,
    s3_key          varchar(256)                       not null,
    file_name       varchar(256)                       not null,
    file_mime       varchar(64)                        not null,
    file_extension  varchar(16)                        not null,
    file_size       int                                not null,
    total_file_size int                                not null,
    image_url_data  json                               not null,
    updated_at      datetime default CURRENT_TIMESTAMP null,
    created_at      datetime default CURRENT_TIMESTAMP null,
    constraint images_images_groups_id_fk
        foreign key (image_group_id) references images_groups (id)
);

