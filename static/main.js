$(function () {
    var Model = Backbone.Model.extend({});

    var Collection = Backbone.Collection.extend({
        model: Model,
        url: '/api/images'
    });
    var collection = new Collection();


    var singleItemTpl = '<div class="item img-thumbnail" data-created_at="<%= item.created_at %>">' +
        '<a class="fancybox" rel="fancybox-thumb" title="<%= item.name %>" href="<%= location.origin %>/serve-image/<%= item.photo %>">' +
        '<img src="<%= location.origin %>/serve-image/<%= item.photo %>" class="" alt="" />' +
        '</a>' +
        '<div class="name"><%= item.name %></div>' +
        '<% if(item.tags.length >0) { %><div>tags: <%= item.tags.join(", ") %></div><% } %>' +
        '</div>';

    var View = Backbone.View.extend({

        mainTpl: _.template(singleItemTpl),

        el: "#list",

        fancyOptions: {
            prevEffect: 'elastic',
            type: 'image',
            nextEffect: 'elastic',
            helpers: {
                title: {
                    type: 'inside'
                },
                thumbs: {
                    width: 50,
                    height: 50
                }
            }
        },

        appendOne: function (data) {
            var html = this.mainTpl({item: data});
            this.$el.prepend(html);
        },

        appendMore: function (data) {
            var that = this;
            var html = _.reduce(data, function (str, item) {
                return str + that.mainTpl({item: item})
            }, '');
            this.$el.append(html);
        },

        render: function () {
            var that = this;
            var html = collection.reduce(function (str, item) {
                return str + that.mainTpl({item: item.toJSON()})
            }, '');
            this.$el.html(html);
            var items = this.$('.item a');
            setTimeout(function () {
                items.fancybox(that.fancyOptions).on('click', function (e) {
                    e.preventDefault();
                });
            }, 100)

        }
    });

    var view = new View();
    collection.fetch().done(function () {
        view.render();
    });

    function upload (file) {
        var deferred = new $.Deferred();
        $.post('/api/images', {name: $('[name="name"]').val(), tags: $('[name="tags"]').val()}).done(function (data) {
            var formData = new FormData();
            if (file) {
                formData.append('photo', file)
            }
            else {
                formData.append('photo', $('[name="photo"]')[0].files[0]);
            }
            formData.append('id', data.id);
            $.ajax({
                type: 'POST',
                url: data.upload_url,
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
                success: function (data) {
                    console.log("success");
                    console.log(data);
                    view.appendOne(data);
                    deferred.resolve();
                },
                error: function (data) {
                    console.log("error");
                    console.log(data);
                    deferred.reject();
                }
            });
        }).fail(function () {
            deferred.reject();
        });
        return deferred.promise();
    }
    $('.btn.create').on('click', function (e) {
        e.preventDefault();
        upload();
    });
    $('.load-more').on('click', function (e) {
        var me = $(e.currentTarget);
        var time = $('.item:last-child').data('created_at');
        if (!time) {
            return;
        }
        $.get('/api/images?from=' + time).done(_.bind(view.appendMore, view)).done(function (data) {
            if (data.length < 20) {
                me.attr('disabled', 'disabled').text('that\'s all');
            }
        });

    });
    (function () {
        var el = $('body,html');
        el.on('dragover',function (e) {
            e.preventDefault();
            e.stopPropagation();
        });
        el.on('dragenter', function (e) {
            e.preventDefault();
            e.stopPropagation();
        });
        el.on('drop', function (e) {
            e.preventDefault();
            e.stopPropagation();
            if (e.originalEvent.dataTransfer) {
                if (e.originalEvent.dataTransfer.files.length) {
                    e.preventDefault();
                    e.stopPropagation();

                    _.each(e.originalEvent.dataTransfer.files, upload);
                }
                else {
                    console.log('drop fail e.originalEvent.dataTransfer.files.length', e.originalEvent.dataTransfer.files.length)
                }
            }
            else {
                console.log('drop fail e.originalEvent.dataTransfer', e.originalEvent.dataTransfer)
            }
        });
    })();

});