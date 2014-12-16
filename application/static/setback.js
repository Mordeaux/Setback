$(function(){
/////////////////////////////////
////MODELS
/////////////////////////////////
var Hand = Backbone.Model.extend({
  defaults: {
    cards: []
  }
});
/////////////////////////////////
////VIEWS
/////////////////////////////////
var HandView = Backbone.View.extend({
  el: '#display',
  handTpl: _.template( $('#hand-template').html()),

  events: {
    
  },
 
  initialize: function() {
    this.$el = $('#display');
  },

  render: function() {
    this.$el.html( this.handTpl( this.model.attributes ) );
    var cards = this.model.attributes.cards;
    for(var i = 0; i < 6; i++){
        var targetDiv = '#card'+i.toString();
        //$(targetDiv).load('/static/images/'+cards[i]+'.svg');
        $(targetDiv).append('<h2>'+cards[i]+'</h2>');
    }
    return this;
  }

});

//  var myHand = new Hand({cards:['10c', '2d', '12s', '14s', '9h', '14h']});
//  var gameView = new HandView({model: myHand});
//  gameView.render();
});
