$(function(){
  App.user = new User({"id": user_id});
  App.user.on({'change':function(){App.topbarView.render();App.dashView.render();}});
  App.topbarView = new TopbarView({model:App.user});
  App.dashView = new DashView({model:App.user});
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
  App.user.fetch();

});
