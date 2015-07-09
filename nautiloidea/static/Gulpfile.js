var gulp = require('gulp'),
    babel = require('gulp-babel'),
    babelify = require('babelify'),
    browserify = require('browserify'),
    source = require('vinyl-source-stream'),
    uglify = require('gulp-uglify'),
    rename = require('gulp-rename');


gulp.task('watch', function(){
    gulp.watch('src/*.jsx', ['default'])
})

gulp.task('default', function(){
    browserify({
        entries: 'src/index.jsx',
        extensions: ['.jsx']
    })
    .transform(babelify)
    .bundle()
    .pipe(source('index.js'))
    .pipe(gulp.dest('dist'));
})

gulp.task('minify', function(){
    gulp.src('dist/index.js')
        .pipe(uglify())
        .pipe(rename('index.min.js'))
        .pipe(gulp.dest('dist'))
})
