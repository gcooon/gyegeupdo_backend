import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models_app', '0002_add_comments_and_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.CharField(
                choices=[('free', '자유토론'), ('product_review', '제품후기'), ('question', '질문')],
                default='free',
                max_length=20,
                verbose_name='태그',
            ),
        ),
        migrations.AddField(
            model_name='post',
            name='product',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='board_posts',
                to='models_app.product',
                verbose_name='관련 제품',
            ),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(
                fields=['category', 'tag', '-created_at'],
                name='models_app__cat_tag_created_idx',
            ),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(
                fields=['product', '-created_at'],
                name='models_app__product_created_idx',
            ),
        ),
    ]
