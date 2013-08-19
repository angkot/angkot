module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    concat: {
      options: {
        separator: ';'
      },
      route: {
        src: [
          'angkot/static/js/Leaflet.Tooltip.js',
          'angkot/static/js/Leaflet.Control.TransportationInfo.js',
          'angkot/static/js/Leaflet.Polyline.Editable.js',
          'angkot/static/js/Leaflet.Angkot.js',
          'angkot/static/js/Leaflet.Angkot.Route.js',
          'angkot/static/js/Bing.js',
          'angkot/static/js/modal.js',
          'angkot/static/js/angkot-map.js',
          'angkot/static/js/angkot-filter.js',
          'angkot/static/js/angkot-route.js',
          'angkot/static/js/angkot-route-menu.js',
          'angkot/static/js/angkot-route-main.js',
          'angkot/static/js/angkot-route-newtransportation.js',
          'angkot/static/js/angkot-route-transportationlist.js',
          'angkot/static/js/angkot-route-dataform.js',
          'angkot/static/js/angkot-route-submissionlist.js'
        ],
        dest: 'dist/route.js'
      }
    },
    uglify: {
      route: {
        options: {
          banner: '/*! <%= pkg.name %> - route - <%= grunt.template.today("isoDateTime") %> */\n'
        },
        files: {
          'dist/route.min.js': ['<%= concat.route.dest %>']
        }
      },
    },
    jshint: {
      files: ['gruntfile.js', 'angkot/static/js/*.js'],
      options: {
        browser: true,
        globals: {
          jQuery: true,
          console: true,
          module: true,
          document: true,
          angular: true
        }
      }
    },
    sass: {
      dist: {
        files: [{
          expand: true,
          cwd: 'angkot/static/css',
          src: ['*.scss'],
          dest: 'dist/css',
          ext: '.css'
        }]
      }
    },
    watch: {
      js: {
        files: ['<%= jshint.files %>'],
        tasks: ['jshint'/*, 'qunit'*/]
      },
      css: {
        files: 'angkot/static/css/*.scss',
        tasks: ['sass', 'copy:css']
      }
    },
    copy: {
      js: {
        files: [
          {src: 'dist/js/route.min.js', dest: 'angkot/static/dist/js/route.min.js'}
        ]
      },
      css: {
        files: [{
          expand: true,
          cwd: 'dist/css',
          src: '*.css',
          dest: 'angkot/static/dist/css'
        }]
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-copy');

  grunt.registerTask('test', ['jshint']);

  grunt.registerTask('default', ['jshint', 'concat', 'uglify', 'sass', 'copy']);

};
