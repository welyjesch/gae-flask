 $script([
  'js/angular.js',
  'js/angular-route.js',
  'js/blog.js'
], function() {
  // when all is done, execute bootstrap angular application
  angular.bootstrap(document, ['wjblog']);
});