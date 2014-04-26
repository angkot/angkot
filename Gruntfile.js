module.exports = function(grunt) {

  pytest_env = process.env;
  pytest_env.ANGKOT_LOCAL_SETTINGS = '.travis/localsettings.py';

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
          'angkot/static/js/Leaflet.Control.Locate.js',
          'angkot/static/js/Leaflet.Polyline.Editable.js',
          'angkot/static/js/Leaflet.Angkot.js',
          'angkot/static/js/Leaflet.Angkot.Route.js',
          'angkot/static/js/Bing.js',
          'angkot/static/js/modal.js',
          'angkot/static/js/angkot.js',
          'angkot/static/js/angkot-utils.js',
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
        dest: 'dist/js/route.js'
      }
    },
    uglify: {
      route: {
        options: {
          banner: '/*! <%= pkg.name %> - route - <%= grunt.template.today("isoDateTime") %> */\n'
        },
        files: {
          'dist/js/route.min.js': ['<%= concat.route.dest %>']
        }
      },
    },
    jshint: {
      files: ['Gruntfile.js', 'angkot/static/js/*.js'],
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
      },
      livereload: {
        options: {
          livereload: true,
        },
        files: ['angkot/static/dist-css/*.css'],
      }
    },
    compress: {
      options: {
        mode: 'gzip',
      },
      js: {
        files: [{
          expand: true,
          cwd: 'dist/js',
          src: ['*.js'],
          dest: 'dist/js',
        }]
      },
      css: {
        files: [{
          expand: true,
          cwd: 'dist/css',
          src: ['*.css'],
          dest: 'dist/css',
        }]
      },
    },
    copy: {
      js: {
        files: [{
          expand: true,
          cwd: 'dist/js',
          src: ['*.js', '*.js.gz'],
          dest: 'angkot/static/dist-js'
        }]
      },
      css: {
        files: [{
          expand: true,
          cwd: 'dist/css',
          src: ['*.css', '*.css.gz'],
          dest: 'angkot/static/dist-css'
        }, {
          expand: true,
          cwd: 'angkot/static/css',
          src: ['*.css', '*.css.gz'],
          dest: 'angkot/static/dist-css'
        }]
      }
    },
    shell: {
      pytest: {
        command: 'py.test angkot',
        options: {
          stdout: true,
          failOnError: true,
          execOptions: {
            env: pytest_env
          },
        },
      },
    },
  });

  grunt.loadNpmTasks('grunt-shell');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-compress');

  grunt.registerTask('pytest', ['shell:pytest']);

  grunt.registerTask('test', ['jshint'/*, 'pytest'*/]);

  grunt.registerTask('default', ['jshint', 'concat', 'uglify', 'sass', 'compress', 'copy']);

};
