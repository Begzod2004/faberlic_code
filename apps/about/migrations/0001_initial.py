# Generated by Django 5.0.7 on 2024-08-04 15:51

import apps.utils
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phone_1",
                    models.CharField(
                        blank=True,
                        max_length=17,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                                regex="^\\+?1?\\d{9,15}$",
                            )
                        ],
                    ),
                ),
                (
                    "phone_2",
                    models.CharField(
                        blank=True,
                        max_length=17,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                                regex="^\\+?1?\\d{9,15}$",
                            )
                        ],
                    ),
                ),
                ("address", models.CharField(max_length=255)),
                ("address_af", models.CharField(max_length=255, null=True)),
                ("address_ar", models.CharField(max_length=255, null=True)),
                ("address_ar_dz", models.CharField(max_length=255, null=True)),
                ("address_ast", models.CharField(max_length=255, null=True)),
                ("address_az", models.CharField(max_length=255, null=True)),
                ("address_bg", models.CharField(max_length=255, null=True)),
                ("address_be", models.CharField(max_length=255, null=True)),
                ("address_bn", models.CharField(max_length=255, null=True)),
                ("address_br", models.CharField(max_length=255, null=True)),
                ("address_bs", models.CharField(max_length=255, null=True)),
                ("address_ca", models.CharField(max_length=255, null=True)),
                ("address_ckb", models.CharField(max_length=255, null=True)),
                ("address_cs", models.CharField(max_length=255, null=True)),
                ("address_cy", models.CharField(max_length=255, null=True)),
                ("address_da", models.CharField(max_length=255, null=True)),
                ("address_de", models.CharField(max_length=255, null=True)),
                ("address_dsb", models.CharField(max_length=255, null=True)),
                ("address_el", models.CharField(max_length=255, null=True)),
                ("address_en", models.CharField(max_length=255, null=True)),
                ("address_en_au", models.CharField(max_length=255, null=True)),
                ("address_en_gb", models.CharField(max_length=255, null=True)),
                ("address_eo", models.CharField(max_length=255, null=True)),
                ("address_es", models.CharField(max_length=255, null=True)),
                ("address_es_ar", models.CharField(max_length=255, null=True)),
                ("address_es_co", models.CharField(max_length=255, null=True)),
                ("address_es_mx", models.CharField(max_length=255, null=True)),
                ("address_es_ni", models.CharField(max_length=255, null=True)),
                ("address_es_ve", models.CharField(max_length=255, null=True)),
                ("address_et", models.CharField(max_length=255, null=True)),
                ("address_eu", models.CharField(max_length=255, null=True)),
                ("address_fa", models.CharField(max_length=255, null=True)),
                ("address_fi", models.CharField(max_length=255, null=True)),
                ("address_fr", models.CharField(max_length=255, null=True)),
                ("address_fy", models.CharField(max_length=255, null=True)),
                ("address_ga", models.CharField(max_length=255, null=True)),
                ("address_gd", models.CharField(max_length=255, null=True)),
                ("address_gl", models.CharField(max_length=255, null=True)),
                ("address_he", models.CharField(max_length=255, null=True)),
                ("address_hi", models.CharField(max_length=255, null=True)),
                ("address_hr", models.CharField(max_length=255, null=True)),
                ("address_hsb", models.CharField(max_length=255, null=True)),
                ("address_hu", models.CharField(max_length=255, null=True)),
                ("address_hy", models.CharField(max_length=255, null=True)),
                ("address_ia", models.CharField(max_length=255, null=True)),
                ("address_ind", models.CharField(max_length=255, null=True)),
                ("address_ig", models.CharField(max_length=255, null=True)),
                ("address_io", models.CharField(max_length=255, null=True)),
                ("address_is", models.CharField(max_length=255, null=True)),
                ("address_it", models.CharField(max_length=255, null=True)),
                ("address_ja", models.CharField(max_length=255, null=True)),
                ("address_ka", models.CharField(max_length=255, null=True)),
                ("address_kab", models.CharField(max_length=255, null=True)),
                ("address_kk", models.CharField(max_length=255, null=True)),
                ("address_km", models.CharField(max_length=255, null=True)),
                ("address_kn", models.CharField(max_length=255, null=True)),
                ("address_ko", models.CharField(max_length=255, null=True)),
                ("address_ky", models.CharField(max_length=255, null=True)),
                ("address_lb", models.CharField(max_length=255, null=True)),
                ("address_lt", models.CharField(max_length=255, null=True)),
                ("address_lv", models.CharField(max_length=255, null=True)),
                ("address_mk", models.CharField(max_length=255, null=True)),
                ("address_ml", models.CharField(max_length=255, null=True)),
                ("address_mn", models.CharField(max_length=255, null=True)),
                ("address_mr", models.CharField(max_length=255, null=True)),
                ("address_ms", models.CharField(max_length=255, null=True)),
                ("address_my", models.CharField(max_length=255, null=True)),
                ("address_nb", models.CharField(max_length=255, null=True)),
                ("address_ne", models.CharField(max_length=255, null=True)),
                ("address_nl", models.CharField(max_length=255, null=True)),
                ("address_nn", models.CharField(max_length=255, null=True)),
                ("address_os", models.CharField(max_length=255, null=True)),
                ("address_pa", models.CharField(max_length=255, null=True)),
                ("address_pl", models.CharField(max_length=255, null=True)),
                ("address_pt", models.CharField(max_length=255, null=True)),
                ("address_pt_br", models.CharField(max_length=255, null=True)),
                ("address_ro", models.CharField(max_length=255, null=True)),
                ("address_ru", models.CharField(max_length=255, null=True)),
                ("address_sk", models.CharField(max_length=255, null=True)),
                ("address_sl", models.CharField(max_length=255, null=True)),
                ("address_sq", models.CharField(max_length=255, null=True)),
                ("address_sr", models.CharField(max_length=255, null=True)),
                ("address_sr_latn", models.CharField(max_length=255, null=True)),
                ("address_sv", models.CharField(max_length=255, null=True)),
                ("address_sw", models.CharField(max_length=255, null=True)),
                ("address_ta", models.CharField(max_length=255, null=True)),
                ("address_te", models.CharField(max_length=255, null=True)),
                ("address_tg", models.CharField(max_length=255, null=True)),
                ("address_th", models.CharField(max_length=255, null=True)),
                ("address_tk", models.CharField(max_length=255, null=True)),
                ("address_tr", models.CharField(max_length=255, null=True)),
                ("address_tt", models.CharField(max_length=255, null=True)),
                ("address_udm", models.CharField(max_length=255, null=True)),
                ("address_ug", models.CharField(max_length=255, null=True)),
                ("address_uk", models.CharField(max_length=255, null=True)),
                ("address_ur", models.CharField(max_length=255, null=True)),
                ("address_uz", models.CharField(max_length=255, null=True)),
                ("address_vi", models.CharField(max_length=255, null=True)),
                ("address_zh_hans", models.CharField(max_length=255, null=True)),
                ("address_zh_hant", models.CharField(max_length=255, null=True)),
                (
                    "email",
                    models.EmailField(
                        max_length=255,
                        unique=True,
                        validators=[django.core.validators.EmailValidator],
                    ),
                ),
                ("map", models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=255, null=True)),
                ("title_af", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ar", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "title_ar_dz",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("title_ast", models.CharField(blank=True, max_length=255, null=True)),
                ("title_az", models.CharField(blank=True, max_length=255, null=True)),
                ("title_bg", models.CharField(blank=True, max_length=255, null=True)),
                ("title_be", models.CharField(blank=True, max_length=255, null=True)),
                ("title_bn", models.CharField(blank=True, max_length=255, null=True)),
                ("title_br", models.CharField(blank=True, max_length=255, null=True)),
                ("title_bs", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ca", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ckb", models.CharField(blank=True, max_length=255, null=True)),
                ("title_cs", models.CharField(blank=True, max_length=255, null=True)),
                ("title_cy", models.CharField(blank=True, max_length=255, null=True)),
                ("title_da", models.CharField(blank=True, max_length=255, null=True)),
                ("title_de", models.CharField(blank=True, max_length=255, null=True)),
                ("title_dsb", models.CharField(blank=True, max_length=255, null=True)),
                ("title_el", models.CharField(blank=True, max_length=255, null=True)),
                ("title_en", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "title_en_au",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "title_en_gb",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("title_eo", models.CharField(blank=True, max_length=255, null=True)),
                ("title_es", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "title_es_ar",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "title_es_co",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "title_es_mx",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "title_es_ni",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "title_es_ve",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("title_et", models.CharField(blank=True, max_length=255, null=True)),
                ("title_eu", models.CharField(blank=True, max_length=255, null=True)),
                ("title_fa", models.CharField(blank=True, max_length=255, null=True)),
                ("title_fi", models.CharField(blank=True, max_length=255, null=True)),
                ("title_fr", models.CharField(blank=True, max_length=255, null=True)),
                ("title_fy", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ga", models.CharField(blank=True, max_length=255, null=True)),
                ("title_gd", models.CharField(blank=True, max_length=255, null=True)),
                ("title_gl", models.CharField(blank=True, max_length=255, null=True)),
                ("title_he", models.CharField(blank=True, max_length=255, null=True)),
                ("title_hi", models.CharField(blank=True, max_length=255, null=True)),
                ("title_hr", models.CharField(blank=True, max_length=255, null=True)),
                ("title_hsb", models.CharField(blank=True, max_length=255, null=True)),
                ("title_hu", models.CharField(blank=True, max_length=255, null=True)),
                ("title_hy", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ia", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ind", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ig", models.CharField(blank=True, max_length=255, null=True)),
                ("title_io", models.CharField(blank=True, max_length=255, null=True)),
                ("title_is", models.CharField(blank=True, max_length=255, null=True)),
                ("title_it", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ja", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ka", models.CharField(blank=True, max_length=255, null=True)),
                ("title_kab", models.CharField(blank=True, max_length=255, null=True)),
                ("title_kk", models.CharField(blank=True, max_length=255, null=True)),
                ("title_km", models.CharField(blank=True, max_length=255, null=True)),
                ("title_kn", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ko", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ky", models.CharField(blank=True, max_length=255, null=True)),
                ("title_lb", models.CharField(blank=True, max_length=255, null=True)),
                ("title_lt", models.CharField(blank=True, max_length=255, null=True)),
                ("title_lv", models.CharField(blank=True, max_length=255, null=True)),
                ("title_mk", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ml", models.CharField(blank=True, max_length=255, null=True)),
                ("title_mn", models.CharField(blank=True, max_length=255, null=True)),
                ("title_mr", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ms", models.CharField(blank=True, max_length=255, null=True)),
                ("title_my", models.CharField(blank=True, max_length=255, null=True)),
                ("title_nb", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ne", models.CharField(blank=True, max_length=255, null=True)),
                ("title_nl", models.CharField(blank=True, max_length=255, null=True)),
                ("title_nn", models.CharField(blank=True, max_length=255, null=True)),
                ("title_os", models.CharField(blank=True, max_length=255, null=True)),
                ("title_pa", models.CharField(blank=True, max_length=255, null=True)),
                ("title_pl", models.CharField(blank=True, max_length=255, null=True)),
                ("title_pt", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "title_pt_br",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("title_ro", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ru", models.CharField(blank=True, max_length=255, null=True)),
                ("title_sk", models.CharField(blank=True, max_length=255, null=True)),
                ("title_sl", models.CharField(blank=True, max_length=255, null=True)),
                ("title_sq", models.CharField(blank=True, max_length=255, null=True)),
                ("title_sr", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "title_sr_latn",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("title_sv", models.CharField(blank=True, max_length=255, null=True)),
                ("title_sw", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ta", models.CharField(blank=True, max_length=255, null=True)),
                ("title_te", models.CharField(blank=True, max_length=255, null=True)),
                ("title_tg", models.CharField(blank=True, max_length=255, null=True)),
                ("title_th", models.CharField(blank=True, max_length=255, null=True)),
                ("title_tk", models.CharField(blank=True, max_length=255, null=True)),
                ("title_tr", models.CharField(blank=True, max_length=255, null=True)),
                ("title_tt", models.CharField(blank=True, max_length=255, null=True)),
                ("title_udm", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ug", models.CharField(blank=True, max_length=255, null=True)),
                ("title_uk", models.CharField(blank=True, max_length=255, null=True)),
                ("title_ur", models.CharField(blank=True, max_length=255, null=True)),
                ("title_uz", models.CharField(blank=True, max_length=255, null=True)),
                ("title_vi", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "title_zh_hans",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "title_zh_hant",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("sub_title", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "sub_title_af",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ar",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ar_dz",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ast",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_az",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_bg",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_be",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_bn",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_br",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_bs",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ca",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ckb",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_cs",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_cy",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_da",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_de",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_dsb",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_el",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_en",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_en_au",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_en_gb",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_eo",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_es",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_es_ar",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_es_co",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_es_mx",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_es_ni",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_es_ve",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_et",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_eu",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_fa",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_fi",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_fr",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_fy",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ga",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_gd",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_gl",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_he",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_hi",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_hr",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_hsb",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_hu",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_hy",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ia",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ind",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ig",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_io",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_is",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_it",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ja",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ka",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_kab",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_kk",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_km",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_kn",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ko",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ky",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_lb",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_lt",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_lv",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_mk",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ml",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_mn",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_mr",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ms",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_my",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_nb",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ne",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_nl",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_nn",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_os",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_pa",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_pl",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_pt",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_pt_br",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ro",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ru",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_sk",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_sl",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_sq",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_sr",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_sr_latn",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_sv",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_sw",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ta",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_te",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_tg",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_th",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_tk",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_tr",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_tt",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_udm",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ug",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_uk",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_ur",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_uz",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_vi",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_zh_hans",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sub_title_zh_hant",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=apps.utils.generate_unique_filename,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Social",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "instagram",
                    models.URLField(
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        validators=[django.core.validators.URLValidator],
                    ),
                ),
                (
                    "facebook",
                    models.URLField(
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        validators=[django.core.validators.URLValidator],
                    ),
                ),
                (
                    "telegram",
                    models.CharField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
            ],
        ),
    ]