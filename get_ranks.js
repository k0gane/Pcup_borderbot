glb = {}
glb.ranks = [[1, 10], [11, 100],[101, 200],[201, 300],[301, 400],[401, 500],[501, 600],[601, 700],[701, 800],
[801, 900],[901, 1000],[1001, 1100],[1101, 1200],[1201, 1300],[1301, 1400],[1401, 1500],[1501, 1600],[1601, 1700],
[1701, 1800],[1801, 1900],[1901, 2000],[2001, 2100],[2101, 2200],[2201, 2300],[2301, 2400],[2401, 2500],[2501, 2600],
[2601, 2700],[2701, 2800],[2801, 2900], [2901, 3000], [9901, 10000]]

glb.characters = []
for(var j=1; j<=23; j++) glb.characters.push(j);
var get_ranking_for = async function(c_id = glb.characters[0].id){
    const ret = [];
 for(const ind in glb.ranks){
   const tup = glb.ranks[ind];
   console.info(tup);
   const got = await i.default.get("fanRankingEvents/" + e + "/rankings", {
                 characterId: c_id,
                 start: tup[0],
                 end: tup[1],
                 isTop: !ind
             }).then(res => res.body.userFanRankingScores);
        ret.push(...got);
   await new Promise(resolve => setTimeout(resolve, 400 + 200 * Math.random()));
 }
    return ret;
}
glb.saved_result = {};
var foo = async function(){
    for(const chara of glb.characters){
        glb.saved_result[chara] = await get_ranking_for(chara);
    }
}
foo();

//copy(JSON.stringify(glb.saved_result, null , "  "))