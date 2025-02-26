# Generated by Django 2.2.3 on 2019-07-10 20:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0021_profile_publish_to_thb'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(verbose_name='Transaction Date')),
                ('proof_receipt_requester', models.ImageField(blank=True, null=True, upload_to=profiles.models.get_image_path, verbose_name="Requester's Transaction Proof")),
                ('requester_review', models.CharField(choices=[('SD', 'Strongly Disagree'), ('D', 'Disagree'), ('N', 'Neutral'), ('A', 'Agree'), ('SA', 'Strongly Agree')], default=None, max_length=2, verbose_name="Requester's Review")),
                ('requester_recommendation', models.TextField(blank=True, default=None, null=True, verbose_name="Requester's recommendation")),
                ('requestee_review', models.CharField(choices=[('SD', 'Strongly Disagree'), ('D', 'Disagree'), ('N', 'Neutral'), ('A', 'Agree'), ('SA', 'Strongly Agree')], default=None, max_length=2, null=True, verbose_name="Requestee's Review")),
                ('requestee_recommendation', models.TextField(blank=True, default=None, null=True, verbose_name="Requestee's recommendation")),
                ('proof_receipt_requestee', models.ImageField(blank=True, null=True, upload_to=profiles.models.get_image_path, verbose_name="Requestee's Transaction Proof")),
                ('is_confirmed', models.NullBooleanField(default=None, verbose_name='Confirmed from Requestee')),
                ('is_verified', models.NullBooleanField(default=None, verbose_name='Verified from Admin')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Transaction Amount')),
                ('currency', models.CharField(choices=[('AED', 'United Arab Emirates dirham'), ('AFN', 'Afghan afghani'), ('ALL', 'Albanian lek'), ('AMD', 'Armenian dram'), ('AOA', 'Angolan kwanza'), ('ARS', 'Argentine peso'), ('AUD', 'Australian dollar'), ('AZN', 'Azerbaijani manat'), ('BAM', 'Bosnia and Herzegovina convertible mark'), ('BBD', 'Barbadian dollar'), ('BDT', 'Bangladeshi taka'), ('BGN', 'Bulgarian lev'), ('BHD', 'Bahraini dinar'), ('BIF', 'Burundian franc'), ('BND', 'Brunei dollar'), ('BOB', 'Bolivian boliviano'), ('BRL', 'Brazilian real'), ('BSD', 'Bahamian dollar'), ('BTN', 'Bhutanese ngultrum'), ('BWP', 'Botswana pula'), ('BYN', 'Belarusian ruble'), ('BZD', 'Belize dollar'), ('CAD', 'Canadian dollar'), ('CDF', 'Congolese franc'), ('CHF', 'Swiss franc'), ('CLP', 'Chilean peso'), ('CNY', 'Chinese yuan'), ('COP', 'Colombian peso'), ('CRC', 'Costa Rican colón'), ('CUP', 'Cuban peso'), ('CVE', 'Cape Verdean escudo'), ('CZK', 'Czech koruna'), ('DJF', 'Djiboutian franc'), ('DKK', 'Danish krone'), ('DOP', 'Dominican peso'), ('DZD', 'Algerian dinar'), ('EGP', 'Egyptian pound'), ('ERN', 'Eritrean nakfa'), ('ETB', 'Ethiopian birr'), ('EUR', 'Euro'), ('FJD', 'Fijian dollar'), ('GBP', 'British pound'), ('GEL', 'Georgian lari'), ('GHS', 'Ghanaian cedi'), ('GMD', 'Gambian dalasi'), ('GNF', 'Guinean franc'), ('GTQ', 'Guatemalan quetzal'), ('GYD', 'Guyanese dollar'), ('HNL', 'Honduran lempira'), ('HRK', 'Croatian kuna'), ('HTG', 'Haitian gourde'), ('HUF', 'Hungarian forint'), ('IDR', 'Indonesian rupiah'), ('ILS', 'Israeli new shekel'), ('INR', 'Indian rupee'), ('IQD', 'Iraqi dinar'), ('IRR', 'Iranian rial'), ('ISK', 'Icelandic króna'), ('JMD', 'Jamaican dollar'), ('JOD', 'Jordanian dinar'), ('JPY', 'Japanese yen'), ('KES', 'Kenyan shilling'), ('KGS', 'Kyrgyzstani som'), ('KHR', 'Cambodian riel'), ('KMF', 'Comorian franc'), ('KPW', 'North Korean won'), ('KRW', 'South Korean won'), ('KWD', 'Kuwaiti dinar'), ('KZT', 'Kazakhstani tenge'), ('LAK', 'Lao kip'), ('LBP', 'Lebanese pound'), ('LKR', 'Sri Lankan rupee'), ('LRD', 'Liberian dollar'), ('LSL', 'Lesotho loti'), ('LYD', 'Libyan dinar'), ('MAD', 'Moroccan dirham'), ('MDL', 'Moldovan leu'), ('MGA', 'Malagasy ariary'), ('MKD', 'Macedonian denar'), ('MMK', 'Burmese kyat'), ('MNT', 'Mongolian tögrög'), ('MRO', 'Mauritanian ouguiya'), ('MUR', 'Mauritian rupee'), ('MVR', 'Maldivian rufiyaa'), ('MWK', 'Malawian kwacha'), ('MXN', 'Mexican peso'), ('MYR', 'Malaysian ringgit'), ('MZN', 'Mozambican metical'), ('NAD', 'Namibian dollar'), ('NGN', 'Nigerian naira'), ('NIO', 'Nicaraguan córdoba'), ('NOK', 'Norwegian krone'), ('NPR', 'Nepalese rupee'), ('NZD', 'New Zealand dollar'), ('OMR', 'Omani rial'), ('PAB', 'Panamanian balboa'), ('PEN', 'Peruvian sol'), ('PGK', 'Papua New Guinean kina'), ('PHP', 'Philippine peso'), ('PKR', 'Pakistani rupee'), ('PLN', 'Polish zloty'), ('PYG', 'Paraguayan guaraní'), ('QAR', 'Qatari riyal'), ('RON', 'Romanian leu'), ('RSD', 'Serbian dinar'), ('RUB', 'Russian ruble'), ('RWF', 'Rwandan franc'), ('SAR', 'Saudi riyal'), ('SBD', 'Solomon Islands dollar'), ('SCR', 'Seychellois rupee'), ('SDG', 'Sudanese pound'), ('SEK', 'Swedish krona'), ('SGD', 'Singapore dollar'), ('SLL', 'Sierra Leonean leone'), ('SOS', 'Somali shilling'), ('SRD', 'Surinamese dollar'), ('SSP', 'South Sudanese pound'), ('STD', 'São Tomé and Príncipe dobra'), ('SYP', 'Syrian pound'), ('SZL', 'Swazi lilangeni'), ('THB', 'Thai baht'), ('TJS', 'Tajikistani somoni'), ('TMT', 'Turkmenistan manat'), ('TND', 'Tunisian dinar'), ('TOP', "Tongan pa'anga"), ('TRY', 'Turkish lira'), ('TTD', 'Trinidad and Tobago dollar'), ('TWD', 'New Taiwan dollar'), ('TZS', 'Tanzanian shilling'), ('UAH', 'Ukrainian hryvnia'), ('UGX', 'Ugandan shilling'), ('USD', 'United States dollar'), ('UYU', 'Uruguayan peso'), ('UZS', 'Uzbekistani som'), ('VEF', 'Venezuelan bolívar'), ('VND', 'Vietnamese dong'), ('VUV', 'Vanuatu vatu'), ('WST', 'Samoan tala'), ('XAF', 'Central African CFA franc'), ('XCD', 'East Caribbean dollar'), ('XOF', 'West African CFA franc'), ('YER', 'Yemeni rial'), ('ZAR', 'South African rand')], default='USD', max_length=3, verbose_name='Transaction Currency')),
                ('is_requester_principal', models.BooleanField(default=False, verbose_name='Requester Payed')),
                ('requestee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requestee', to=settings.AUTH_USER_MODEL, verbose_name='Requestee')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester', to=settings.AUTH_USER_MODEL, verbose_name='Requester')),
            ],
        ),
    ]
