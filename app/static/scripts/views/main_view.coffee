define ['static/scripts/vendor/text!static/scripts/templates/main_template.html'],
  (template) ->
    class MainView extends Backbone.View
      events:
        'click a.home'  : 'index'
        'click a.login' : 'login'
        'click a.logout': 'logout'
      index: (e) ->
        e.preventDefault()
        window.router.navigate '', {trigger: true}
      login: (e) ->
        e.preventDefault()
        window.router.navigate 'login', {trigger: true}
      logout: (e) ->
        e.preventDefault()
        @model.attributes.logged_in = false
        window.router.navigate 'login', {trigger: true}
      render: ->
        compiled = _.template template, @model.toJSON()
        @$el.html compiled
        return @

    return {view: MainView}
