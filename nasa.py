// GEE script: per-pixel peak NDVI day-of-year (Landsat 8 Surface Reflectance)
// Paste into: https://code.earthengine.google.com

var geometry = /* color: #d63000 */ ee.Geometry.Polygon(
        [[[77.0, 28.9],
          [77.0, 28.5],
          [77.6, 28.5],
          [77.6, 28.9]]]); // edit to your AOI

var year = 2024;
var start = ee.Date.fromYMD(year,1,1);
var end = ee.Date.fromYMD(year,12,31);

var collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
  .filterBounds(geometry)
  .filterDate(start, end)
  .map(function(img){
    // simple cloud mask using pixel_qa
    var qa = img.select('pixel_qa');
    var cloudShadow = qa.bitwiseAnd(1 << 3).neq(0);
    var clouds = qa.bitwiseAnd(1 << 5).neq(0);
    var mask = clouds.or(cloudShadow).not();
    img = img.updateMask(mask);
    // compute NDVI
    var ndvi = img.normalizedDifference(['B5','B4']).rename('NDVI')
      .multiply(10000).toInt16(); // scaled for storage
    return img.addBands(ndvi).copyProperties(img,['system:time_start']);
  });

// compute image of max NDVI and date of max NDVI
var ndviMax = collection.qualityMosaic('NDVI').select('NDVI');
var ndviMaxDate = collection
  .map(function(img){
    // create an image with constant = time in days-of-year when this image NDVI equals stack NDVI
    var doy = ee.Date(img.get('system:time_start')).getRelative('day','year').add(1);
    var equalMax = img.select('NDVI').eq(ndviMax);
    // where equalMax true set to doy otherwise 0
    return equalMax.multiply(doy).rename('doy').int16();
  })
  .max(); // pixel will have the highest doy where NDVI equals max (handles multiple obs)

// Visualize
Map.centerObject(geometry, 11);
Map.addLayer(ndviMax.visualize({min:2000, max:9000, palette:['white','green']}), {}, 'Peak NDVI (scaled)');
Map.addLayer(ndviMaxDate, {min:1, max:365, palette:['purple','blue','green','yellow','red']}, 'DOY of Peak NDVI');

// export example
Export.image.toDrive({
  image: ndviMaxDate.clip(geometry),
  description: 'peak_ndvi_doy_'+year,
  scale: 30,
  region: geometry,
  maxPixels: 1e9
});
