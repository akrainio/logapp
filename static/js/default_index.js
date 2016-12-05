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

    // Enumerates an array.
    var enumerate = function(v) {
        var k=0;
        return v.map(function(e) {e._idx = k++;});
    };

    self.get_stamps = function() {
        // Add post request sent
        $.post(get_stamps_url,
            {
                start_stamp: self.vue.start_stamp,
                end_stamp: self.vue.end_stamp,
                folder: self.vue.folders[self.vue.selected]
            },
            function (data) {
                self.vue.output = (data.parsed).join("\n");
                self.vue.has_output = true
            });
    };

    self.toggle_namer = function () {
        self.vue.namer = !self.vue.namer;
        if (!self.vue.namer) {
            self.vue.naming_failure = false;
            self.vue.new_folder_name = null;
        }
    };

    self.get_folders = function () {
        $.getJSON(get_folders_url, function (data) {
            self.vue.folders = data.folders;
            enumerate(self.vue.folders);
        })
    };

    self.mk_folder = function () {
        $.post(add_folder_url,
            {
                new_folder_name: self.vue.new_folder_name
            },
            function (data) {
                if (data.succeeded) {
                    self.vue.folders.push(self.vue.new_folder_name);
                    self.toggle_namer();
                    self.vue.new_folder_name = null;
                    self.vue.naming_failure = false;
                } else {
                    self.vue.naming_failure = true;
                }
            });

    };

    self.delete_folder = function (index) {
        var folder_name = self.vue.folders[index];
        if (self.vue.selected == index) {
            self.vue.selected = 0;
        }
        $.post(delete_folder_url,
            {
                folder_name: folder_name
            },
            function (data) {
                self.get_folders()
            });
    };

    self.is_selected = function(index) {
        return index == self.vue.selected;
    };

    self.select_folder = function (index) {
        self.vue.selected = index;
    };

    self.get_selected = function () {
        console.log(self.vue.folders);
        return self.vue.folders[self.vue.selected]
    };


    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            selected: 0,
            folders: [],
            output: null,
            has_output: false,
            start_stamp: null,
            end_stamp: null,
            new_folder_name: null,
            text_area: null,
            naming_failure: false,
            namer: false
        },
        methods: {
            get_stamps: self.get_stamps,
            mk_folder: self.mk_folder,
            toggle_namer: self.toggle_namer,
            is_selected: self.is_selected,
            select_folder: self.select_folder,
            get_selected: self.get_selected,
            delete_folder: self.delete_folder,
        }

    });

    self.get_folders();
    $("#vue-div").show();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
