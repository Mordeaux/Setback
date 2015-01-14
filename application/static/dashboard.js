$(function(){
  var user = new User({"id": user_id});
  var topbarView = new TopbarView({model:user});
  var dashView = new DashView({model:user});
  App.wait = function(){
    console.log(this);
    console.log(this.current_game.get('turn'));
    console.log(this.current_game.get('player_number'));
    console.log(this.current_game.get('turn') != this.current_game.get('player_number'));
    if (this.current_game.get('turn') != this.current_game.get('player_number')){
      console.log('while');
      console.log(App.current_game.get('last_mod'));
      console.log(App.current_game.url()+'?timestamp='+encodeURIComponent(App.current_game.get('last_mod')));
      App.interval = setInterval(function (){
        console.log('working');
        $.get(App.current_game.url()+'?timestamp='+encodeURIComponent(App.current_game.get('last_mod')), function(data){
          console.log(data);
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
