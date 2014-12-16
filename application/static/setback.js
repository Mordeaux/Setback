$(function(){
/////////////////////////////////
////MODELS
/////////////////////////////////
var Game = Backbone.Model.extend({
  defaults: {
    cards: []
  }
});
/////////////////////////////////
////COLLECTIONS
/////////////////////////////////
var GameCollection = Backbone.Collection.extend({
  model: Game,
  url: '/game',

  parse: function(resp) {
    console.log('eeee');
    console.log(resp);
    return resp;
  }
});
/////////////////////////////////
////VIEWS
/////////////////////////////////
var GameView = Backbone.View.extend({
  el: '#display',
  handTpl: _.template( $('#hand-template').html()),
  sidebarTpl: _.template( $('#sidebar-template').html()),
  gameboardTpl: _.template( $('#gameboard-template').html()),

  events: {
    
  },
 
  initialize: function() {
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

    var games = new GameCollection();
    console.log(games);
    games.fetch();
//  var myHand = new Hand({cards:['10c', '2d', '12s', '14s', '9h', '14h']});
//  var gameView = new HandView({model: myHand});
//  gameView.render();
});
