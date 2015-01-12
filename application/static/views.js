/////////////////////////////////
////MODELS
/////////////////////////////////

var Game = Backbone.Model.extend({});

/////////////////////////////////

var User = Backbone.Model.extend({
    url: function () {
        return '/user/'+this.id;
    }
});

/////////////////////////////////
////VIEWS
/////////////////////////////////

var TopbarView = Backbone.View.extend({
  el: '#topbar',
  topbarTpl: _.template( $('#topbar-template').html()),

  render: function() {
    this.$el.html( this.topbarTpl( this.model.attributes ) );
    this.$('#games-list').append( this.model.attributes.games);
    return this;
  }
});

/////////////////////////////////

var DashView = Backbone.View.extend({
  el: '#display',
  dashTpl: _.template( $('#dash-template').html()),

  render: function () {
    this.$el.html( this.dashTpl( this.model.attributes ) );
    for(i=0;i<this.model.attributes.games.length;i++){
      this.$('#game_'+this.model.attributes.games[i]).click(function(){
        var games = new GameCollection();
        var games_id = parseInt(this.id.slice(5));
        games.fetch({success:function(m,r,o){
          var gameView = new GameView({'model':games.get(games_id)}).render();
        }});
      });
    }
    return this;
  }
});

/////////////////////////////////

var GameView = Backbone.View.extend({
  el: '#display',
  handTpl: _.template( $('#hand-template').html()),
  sidebarTpl: _.template( $('#sidebar-template').html()),
  gameboardTpl: _.template( $('#gameboard-template').html()),

  render: function() {
    this.$el.html( this.gameboardTpl( this.model.attributes ) );
    var cards = this.model.attributes.hand;
    console.log(this.model.attributes.usernames);
//    for(var i = 0; i < cards.length; i++){
//        var targetDiv = '#card'+i.toString();
//        //$(targetDiv).load('/static/images/'+cards[i]+'.svg');
//        $(targetDiv).append('<h2>'+cards[i]+'</h2>');
//    }
    return this;
  }
});

/////////////////////////////////
////COLLECTIONS
/////////////////////////////////

var GameCollection = Backbone.Collection.extend({
  model: Game,
  url: '/game',

  parse: function(response){
    return response.models
  }
});

