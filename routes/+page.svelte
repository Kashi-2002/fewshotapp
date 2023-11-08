<style>
    h1{
        text-align: center;
        margin: 24px;
    }
    .group{
        text-align: center;
    margin-top: 25px;
    }
</style>

 
<h1>Convert handwritten pdf to typed text.</h1>
<form id="myForm" method="post" action="/" enctype="multipart/form-data">
    <div class="group">
      <label for="file">Upload the sample files here.</label>
    <!-- <h2>Upload the sample files here.</h2> -->
      <input
        type="file"
        id="samples"
        name="fileToUploads"
      />

      <button type="submit" id="sample">Submit</button>

</div>
  </form>

  <form id="myForms" method="post" action="/" enctype="multipart/form-data">
    <div class="group">
      <label for="file">Upload the target files here.</label>
      <input
      type="file"
      id="target"
      name="fileToUpload"
    />
    
    <button type="submit" id="targ">Submit</button>


</div>
  </form>
  <h2 style="text-align: center;">Click on below submit button after uploading both the folders.</h2>
  <button type="submit" style="position: relative;
  left: 583px;
  top: 30px;" on:click={()=>cropimages()}>Submit</button>


<script>
    function cropimages(){
      console.log("clicked")
      // window.location.reload("http://127.0.0.1:8000/su");
      // location.href = "http://127.0.0.1:8000/su"; 
      // location.reload();
        fetch("http://127.0.0.1:8000/" )
    .then(async(response) => {
      let clone = response.clone();
      let res = await clone.json();
      // console.log(res);
      if(res["output"]=="success"){
        alert("Check your folder cropped. This contains the cropped images!")
      }
      
      // const parsedData = parse(clone);
    })
    }
</script>

