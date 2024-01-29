var gtype;
function selectgraph(e){
    var id = e.target.getAttribute("id");
    if(id == "views"){
        gtype = "view_count";
        $("#graphtype").text("Views")
    }
    else{
        gtype = "like_count";
        $("#graphtype").text("Likes")
    }
}
function cb(){
    n = document.getElementById('nvalue').value
    //gtype = document.getElementById('graphtype').value
    $.getJSON({
        url: "/callback", data:{'nval': n, 'yval' : gtype}, success: function(result){
            Plotly.newPlot('chart',result,{})
        }
    })
}
d = {{ graphJSON | safe}};
Plotly.newPlot('chart', d, {});