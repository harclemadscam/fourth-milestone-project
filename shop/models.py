from django.db import models
from django.urls import reverse


#  Use of slugs taken from Chapter 7 of book
# "Django 3 By Example" by Antonio Melé
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    friendly_name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


# Use of slugs and get url methods largely taken from Chapter 7 of book
# "Django 3 By Example" by Antonio Melé
class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True,
                                 related_name='products',
                                 on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image1 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    image2 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    image3 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    image4 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(null=True, blank=True)
    customisable = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=6, decimal_places=2,
                                 null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_details',
                       args=[self.id, self.slug])

    def get_edit_product_url(self):
        return reverse('edit_product',
                       args=[self.id, self.slug])

    def get_delete_product_url(self):
        return reverse('delete_product',
                       args=[self.id, self.slug])

    def get_create_review_url(self):
        return reverse('create_product_review',
                       args=[self.id, self.slug])

    def get_edit_review_url(self):
        return reverse('edit_product_review',
                       args=[self.id, self.slug])

    def get_delete_review_url(self):
        return reverse('delete_product_review',
                       args=[self.id, self.slug])

    def calculate_rating(self):
        product_rating = 0
        if self.product_reviews:
            reviews = self.product_reviews.all()
            total_of_ratings = sum(review.rating for review in reviews)
            number_of_reviews = reviews.__len__()
            if number_of_reviews == 0:
                self.rating = product_rating
                self.save()
                return self.rating
            else:
                product_rating = total_of_ratings / number_of_reviews
                self.rating = product_rating
                self.save()
                return self.rating
        return product_rating
