// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };


    self.get_stamps = function() {
        // Add post request sent
        $.post(get_stamps_url,
            {
                start_stamp: self.vue.start_stamp,
                end_stamp: self.vue.end_stamp
            },
            function (data) {
                console.log(data.parsed)
            });
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            folders: [],
            start_stamp: null,
            end_stamp: null
        },
        methods: {
            get_stamps: self.get_stamps
        }

    });

    $("#vue-div").show();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
