window.onload = init(undefined);


function reload_canvas(textureAddress){
    // clear all the already-exist 3D canvas
    $("#webgl-output").empty();

    // init a new 3D model canvas
    init(textureAddress);
}


function init(textureAddress)
{
    // create background
    var scene = new THREE.Scene();
    // set camera
    var camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 8000);
    // create renderer
    var renderer = new THREE.WebGLRenderer();
    // set renderer's basic color
    renderer.setClearColor(new THREE.Color(0xeeeeee));
    // set canvas' size
    renderer.setSize(window.innerWidth/2.5, window.innerHeight/2.5);
    // render object shadow
    renderer.shadowMap.enabled = true;
    // show 3d coordinate
    var axes = new THREE.AxesHelper(20);

    // add coordinate to scene
    scene.add(axes);

    // create ground geometry
    // var planeGeometry = new THREE.PlaneGeometry(60,20);
    // // set color to ground
    // var planeMaterial = new THREE.MeshStandardMaterial({color: 0xcccccc});
    // // create ground geometry (bind geometry and material)
    // var plane = new THREE.Mesh(planeGeometry, planeMaterial);
    // // move object's location
    // plane.rotation.x = -0.5 * Math.PI;
    // plane.position.x = 0;
    // plane.position.y = 0;
    // plane.position.z = 0;
    // plane.castShadow = true;
    // // receive shadow
    // plane.receiveShadow = true;
    // add ground to scene
    // scene.add(plane);

    // // add a cube
    // var cubeGeometry = new THREE.BoxGeometry(4, 4, 4);
    // var cubeMaterial = new THREE.MeshLambertMaterial({color: 0xff0000});
    // var cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
    // //
    // cube.position.x = 0;
    // cube.position.y = 4;
    // cube.position.z = 2;
    //
    // // add a sphere
    // var sphereGeometry = new THREE.SphereGeometry(4, 20, 20);
    // var sphereMaterial = new THREE.MeshLambertMaterial({color: 0xff0000});
    // var sphere = new THREE.Mesh(sphereGeometry, sphereMaterial)
    //
    // sphere.position.x = 10;
    // sphere.position.y = 4;
    // sphere.position.z = 0;


    // render shadow
    // sphere.castShadow = true;
    // cube.castShadow = true;
    // scene.add(sphere);
    // scene.add(cube);

    // obj loader
    // var loader = new THREE.OBJLoader();
    // // objLoader.setPath('/');
    // loader.load("./saxphone.obj", function (obj) {
    //     //obj.translationX(10);
    //     // obj.translationY(-200);
    //     // obj.translationZ(-30);
    //     scene.add(obj);
    // });

    // get the default texture without customization
    if (textureAddress === undefined){
        textureAddress = $("#modeltype-3d-model").attr("model-texture-address");
    }

    let texturePlant = new THREE.TextureLoader().load(textureAddress);//模型贴图
    console.log("texture");
    console.log(texturePlant);
    let modelAddress = $("#modeltype-3d-model").attr("model-address");
    var loader = new THREE.FBXLoader();//创建一个FBX加载器
    // loader.load("/static/upload/model_type/3d-model-files/pre-store/cello.fbx", function (obj)
    loader.load(modelAddress, function (obj)
    {
        console.log(obj);//查看加载后返回的模型对象


        obj.traverse(function (child)
        {

            var material = new THREE.MeshPhongMaterial({
                map: texturePlant
            });
            child.material = material;
            if (child.isMesh)
            {
                child.castShadow = true;
                child.receiveShadow = true;

            }
            ;

        });


        scene.add(obj)
        // 适当平移fbx模型位置
        obj.translateX(580);
        obj.translateY(-200);
        obj.translateZ(-30);
        // obj.rotateY(0.5 * Math.PI);
    })


    // create ambient light source
    const ambientLight = new THREE.AmbientLight(0xcccccc, 0.4);
    scene.add(ambientLight);

    // create parallel light
    var light = new THREE.DirectionalLight(0xffffff);
    light.position.set(-130, 130, 130);
    light.castShadow = false;
    scene.add(light)

    // create spot light source
    var spotLight = new THREE.SpotLight(0xFFFFFF);
    // set light position
    spotLight.position.set(130, 130, -130);
    spotLight.castShadow = true;

    //light source spread
    spotLight.angle = Math.PI / 10;
    // set ray-tracing percent
    spotLight.shadow.penumbera = 0.05;

    // set shadow precision
    spotLight.shadow.mapSize.width = 4096;
    spotLight.shadow.mapSize.height = 4096;

    camera.add(spotLight);


    // locate camera and point to the center of scene
    camera.position.x = 0;
    camera.position.y = 0;
    camera.position.z = 50;
    camera.lookAt(scene.position);

    // add renderer's output to html page
    document.getElementById('webgl-output').appendChild(renderer.domElement);
    renderer.render(scene, camera);

    let t0 = new Date()

    // rotate cube
    // function render()
    // {
    //     let t1 = new Date();
    //     let t = t1 - t0;
    //     t0 = t1;
    //     renderer.render(scene, camera);
    //     // 0.001 rad each 1 ms around the y-axis
    //     cube.rotateY(0.001 * t);
    //     window.requestAnimationFrame(render);
    // }

    // // render once every 16 ms
    // setInterval(render, 16)

    // window.requestAnimationFrame(render);

    // create controls object
    var controls = new THREE.OrbitControls(camera, renderer.domElement);
    // liston the mouse action
    controls.addEventListener('change', () =>
    {
        renderer.render(scene, camera);
    })
}