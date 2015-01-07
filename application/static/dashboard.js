$(function(){
  var user = new User({"id": user_id});
  var topbarView = new TopbarView({model:user});
  var dashView = new DashView({model:user});
  user.fetch({
    success: function (m,r,o){
      topbarView.render();
      dashView.render();
     }
   });
});
