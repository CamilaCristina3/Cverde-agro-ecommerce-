from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_add_two_factor_if_missing"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS `users_emailverificationtoken` (
                `id` bigint NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `user_id` bigint NOT NULL,
                `token` char(32) NOT NULL,
                `created_at` datetime NOT NULL,
                `used_at` datetime DEFAULT NULL,
                UNIQUE KEY `users_emailverificationtoken_token_uniq` (`token`),
                KEY `users_emailverificationtoken_user_id_idx` (`user_id`),
                CONSTRAINT `users_emailverificationtoken_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            reverse_sql="""
            DROP TABLE IF EXISTS `users_emailverificationtoken`;
            """,
        ),
    ]
