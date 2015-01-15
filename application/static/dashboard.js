$(function(){
  var user = new User({"id": user_id});
  var topbarView = new TopbarView({model:user});
  var dashView = new DashView({model:user});
  App.wait = function(){
    if (this.current_game.get('turn') != this.current_game.get('player_number')){
      clearInterval(App.interval);
      App.interval = setInterval(function (){
        $.get(App.current_game.url()+'?timestamp='+encodeURIComponent(App.current_game.get('last_mod')), function(data){
          App.current_game.set(data);
        });
      }, 3000);
    }
    else {
      clearInterval(App.interval);
    }
  };
  user.fetch({
    success: function (m,r,o){
      topbarView.render();
      dashView.render();
    }
  });
});
