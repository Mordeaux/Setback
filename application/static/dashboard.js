$(function(){
/////////////////////////////////
////MODELS
/////////////////////////////////
var User = Backbone.Model.extend({
  defaults: {
    games:[]
  }
});
/////////////////////////////////
////VIEWS
/////////////////////////////////
var TopbarView = Backbone.View.extend({
  el: '#topbar',
  topbarTpl: _.template( $('#topbar-template').html()),

  initialize: function() {
  },

  render: function() {
    this.$el.html( this.topbarTpl( this.model.attributes ) );
    this.$('#games-list').append( this.model.attributes.games);
    return this;
  }
});

var DashView = Backbone.View.extend({
  el: '#display',
  dashTpl: _.template( $('#dash-template').html()),

  initialize: function (){
  },

  render: function () {
    this.$el.html( this.dashTpl( this.model.attributes ) );
    return this;
  }
});

  var user = new User({games:['first game', 'second game']});
  var topbarView = new TopbarView({model:user});
  topbarView.render();
});
