# Generated manually for PostComment index optimization

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models_app', '0005_add_post_category_notice_index'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='postcomment',
            index=models.Index(fields=['post', '-created_at'], name='models_app__post_cr_idx'),
        ),
        migrations.AddIndex(
            model_name='postcomment',
            index=models.Index(fields=['parent'], name='models_app__parent_idx'),
        ),
    ]
