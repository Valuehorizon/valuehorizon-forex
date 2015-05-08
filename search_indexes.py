import datetime
from haystack import indexes
from forex.models import Currency




class CurrencyIndex(indexes.SearchIndex, indexes.Indexable):  # use RealTimeSearchIndex for realtime indexing
    text = indexes.CharField(document=True, use_template=True)
    symbol = indexes.CharField(model_attr='symbol')
    name = indexes.CharField(model_attr='name')
    
    # We add this for autocomplete.
    content_auto = indexes.EdgeNgramField(model_attr='name')
    
    # For easy faceting
    #facet_model_name = indexes.CharField(faceted=True)
    
    def get_model(self):
        return Currency
    
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    
    #def prepare_facet_model_name(self, obj):
        #return "Stock"  
    
    
