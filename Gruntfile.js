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
          'static/js/Leaflet.Tooltip.js',
          'static/js/Leaflet.Control.TransportationInfo.js',
          'static/js/Leaflet.Control.Locate.js',
          'static/js/Leaflet.Polyline.Editable.js',
          'static/js/Leaflet.Angkot.js',
          'static/js/Leaflet.Angkot.Route.js',
          'static/js/Bing.js',
          'static/js/modal.js',
          'static/js/angkot.js',
          'static/js/angkot-utils.js',
          'static/js/angkot-map.js',
          'static/js/angkot-filter.js',
          'static/js/angkot-route.js',
          'static/js/angkot-route-menu.js',
          'static/js/angkot-route-main.js',
          'static/js/angkot-route-newtransportation.js',
          'static/js/angkot-route-transportationlist.js',
          'static/js/angkot-route-dataform.js',
          'static/js/angkot-route-submissionlist.js'
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
      files: ['Gruntfile.js', 'static/js/*.js'],
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
          cwd: 'static/css',
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
        files: 'static/css/*.scss',
        tasks: ['sass', 'copy:css']
      },
      livereload: {
        options: {
          livereload: true,
        },
        files: ['static/dist-css/*.css'],
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
          dest: 'static/dist-js'
        }]
      },
      css: {
        files: [{
          expand: true,
          cwd: 'dist/css',
          src: ['*.css', '*.css.gz'],
          dest: 'static/dist-css'
        }, {
          expand: true,
          cwd: 'static/css',
          src: ['*.css', '*.css.gz'],
          dest: 'static/dist-css'
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
