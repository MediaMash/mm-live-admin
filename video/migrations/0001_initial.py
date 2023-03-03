# Generated by Django 3.2.16 on 2023-03-03 23:28

from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0003_alter_productimage_alt'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, choices=[('YouTube', 'YouTube'), ('Twitch', 'Twitch'), ('Facebook', 'Facebook'), ('Internal Premium', 'Amazon'), ('Internal', 'CloudFlare'), ('TikTok', 'TikTok')], help_text='Name of Streaming Provider (YouTube, Twitch etc.)', max_length=255, null=True)),
                ('link', models.CharField(blank=True, help_text='Link to Video Source', max_length=255, null=True)),
                ('token', models.CharField(blank=True, help_text='Auth Token', max_length=255, null=True)),
                ('account_key', models.CharField(blank=True, help_text='Account Key or ID, or API KEY', max_length=255, null=True)),
                ('auth_email', models.CharField(blank=True, help_text='Authorized email of account admin', max_length=255, null=True)),
                ('stream_key', models.CharField(blank=True, help_text='Unique key for streaming', max_length=255, null=True)),
                ('stream_user_name', models.CharField(blank=True, help_text='Authorized username from stream account', max_length=255, null=True)),
                ('stream_region', models.CharField(blank=True, help_text='Twitch or similar region', max_length=255, null=True)),
                ('api_url', models.CharField(blank=True, help_text='API Url', max_length=255, null=True)),
                ('premium', models.BooleanField(blank=True, help_text='Premium or Pay-Per-View Provider', max_length=255, null=True)),
                ('external', models.BooleanField(blank=True, help_text='Extneral or Internal Provider', max_length=255, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Provider',
                'verbose_name_plural': 'Providers',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProviderVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Name of Video', max_length=255, null=True)),
                ('link', models.CharField(blank=True, help_text='Link to Video Source', max_length=255, null=True)),
                ('provider_id_num', models.CharField(blank=True, help_text='ID # From Streaming Host Provider', max_length=255, null=True)),
                ('embed_code', models.CharField(blank=True, help_text='Code used to stream from ebeded player', max_length=255, null=True)),
                ('status', models.CharField(blank=True, help_text='Status of Streaming Video', max_length=255, null=True)),
                ('stream_id', models.CharField(blank=True, help_text='Streaming Provider ID', max_length=255, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('provider', models.ForeignKey(blank=True, help_text='Extneral or Internal Stream Host', null=True, on_delete=django.db.models.deletion.CASCADE, to='video.provider')),
            ],
            options={
                'verbose_name': 'Provider Video',
                'verbose_name_plural': 'Provider Videos',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Name of Video', max_length=255, null=True)),
                ('run_time_minutes', models.CharField(blank=True, help_text='Length of Video Minutes', max_length=255, null=True)),
                ('run_time_seconds', models.CharField(blank=True, help_text='Length of Video Seconds', max_length=255, null=True)),
                ('link', models.CharField(blank=True, help_text='Link to Video Source', max_length=255, null=True)),
                ('video_file', models.FileField(blank=True, help_text='Upload Video', max_length=255, null=True, storage=django.core.files.storage.FileSystemStorage(location='/Users/greglind/Projects/mediamash/mm-live-admin/media/videos/'), upload_to='')),
                ('description', models.TextField(blank=True, help_text='Description of Video', null=True)),
                ('embed_code', models.CharField(blank=True, help_text='Code used to stream from ebeded player', max_length=255, null=True)),
                ('status', models.CharField(blank=True, help_text='Status of Streaming Video', max_length=255, null=True)),
                ('stream_id', models.CharField(blank=True, help_text='Streaming Provider ID', max_length=255, null=True)),
                ('stream_url', models.CharField(blank=True, help_text='Streaming Provider URL', max_length=255, null=True)),
                ('playback_hls', models.CharField(blank=True, help_text='Streaming Provider URL for HLS stream', max_length=255, null=True)),
                ('playback_dash', models.CharField(blank=True, help_text='Streaming Provider URL for DASH stream', max_length=255, null=True)),
                ('is_live', models.BooleanField(default=False)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('direct_provider', models.ManyToManyField(blank=True, help_text='Internal Streaming Host Provider Videos', related_name='direct_provider', to='video.ProviderVideo')),
                ('external_provider', models.ManyToManyField(blank=True, help_text='External/Social Provider Shares', related_name='external_provider', to='video.ProviderVideo')),
                ('owner', models.ForeignKey(blank=True, help_text='User who is the Owner of the Video', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('related_products', models.ManyToManyField(related_name='videos', to='shop.Product')),
            ],
            options={
                'verbose_name': 'Video',
                'verbose_name_plural': 'Videos',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='VideoProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_timestamp', models.CharField(blank=True, help_text='When to display product in Video Minutes', max_length=255, null=True)),
                ('hide_timestamp', models.CharField(blank=True, help_text='When to hide the product in Video Seconds', max_length=255, null=True)),
                ('product', models.ForeignKey(blank=True, help_text='Product to link to Video', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video_products', to='shop.product')),
                ('video', models.ForeignKey(blank=True, help_text='Video', null=True, on_delete=django.db.models.deletion.CASCADE, to='video.video')),
            ],
        ),
        migrations.CreateModel(
            name='LiveStream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Name of Channel', max_length=255, null=True)),
                ('link', models.CharField(blank=True, help_text='Link to Video Source', max_length=255, null=True)),
                ('live_feed_url', models.FileField(blank=True, help_text='Video Stream Feed', max_length=255, null=True, storage=django.core.files.storage.FileSystemStorage(location='/Users/greglind/Projects/mediamash/mm-live-admin/media/videos/'), upload_to='')),
                ('live_feed_token', models.FileField(blank=True, help_text='Video Stream Auth Token', max_length=255, null=True, storage=django.core.files.storage.FileSystemStorage(location='/Users/greglind/Projects/mediamash/mm-live-admin/media/videos/'), upload_to='')),
                ('description', models.TextField(blank=True, help_text='Description of Channel', null=True)),
                ('embed_code', models.CharField(blank=True, help_text='Code used to stream to ebeded player', max_length=255, null=True)),
                ('status', models.CharField(blank=True, help_text='Status of Streaming Channel', max_length=255, null=True)),
                ('stream_id', models.CharField(blank=True, help_text='Streaming Provider ID', max_length=255, null=True)),
                ('stream_url', models.CharField(blank=True, help_text='Streaming Provider URL', max_length=255, null=True)),
                ('playback_hls', models.CharField(blank=True, help_text='Streaming Provider URL for HLS stream', max_length=255, null=True)),
                ('playback_dash', models.CharField(blank=True, help_text='Streaming Provider URL for DASH stream', max_length=255, null=True)),
                ('is_live', models.BooleanField(default=False)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('direct_provider', models.ManyToManyField(blank=True, help_text='Internal Streaming Host Provider Videos', related_name='stream_direct_provider', to='video.ProviderVideo')),
                ('external_provider', models.ManyToManyField(blank=True, help_text='External/Social Provider Shares', related_name='stream_external_provider', to='video.ProviderVideo')),
                ('owner', models.ForeignKey(blank=True, help_text='User who is the Owner of the Video', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'LiveStreams',
                'verbose_name_plural': 'LiveStreams',
                'ordering': ('name',),
            },
        ),
    ]
