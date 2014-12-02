$(function(){
var Hand = Backbone.Model.extend({
  defaults: {
    cards: []
    }
});

var HandView = Backbone.View.extend({
  tagName: 'li',
  handTpl: _.template( $('#hand-template').html()),

  events: {
    
  },
 
  initialize: function() {
    this.$el = $('#hand');
  },

  render: function() {
    this.$el.html( this.handTpl( this.model.attributes ) );
    this.input = this.$('.edit');
    var cards = this.model.attributes.cards;
    for(var i = 0; i < 6; i++){
        var targetDiv = '#card'+i.toString();
        $(targetDiv).load('/static/images/'+cards[i]+'.svg');
    }
    return this;
  }

});

  var myHand = new Hand({cards:['10c', '2d', '12s', '14s', '9h', '14h']});
  var handView = new HandView({model: myHand});
  handView.render();
});
