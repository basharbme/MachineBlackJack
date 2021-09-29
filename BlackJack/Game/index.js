var victories = 0;
$('#game_section').hide();
function update_rec(data){
    return "<p> Hit: "+data['hit']+"</p>"+
    "<p> Stay: "+data['stay']+"</p>";
}
function update_state(game){
    let dealer_card = '';
    let own_card = '';
    for (card of game['self']){
        card = JSON.parse(card)
        own_card+='<div class="card">'+card.card_name+'</div>';
    }
    for (card of game['dealer']){
        card = JSON.parse(card)
        dealer_card+='<div class="card">'+card.card_name+'</div>';
    }
    document.getElementById('dealer_cards_container').innerHTML = dealer_card;
    document.getElementById('own_cards_container').innerHTML = own_card;
    $('#vict').html(victories);
    $.get( "advice", function( data ) {
        data = JSON.parse(data)
        $('#prob_rec').html(update_rec(data.prob_rec));
        $('#ai_rec').html(update_rec(data.ai_rec));
        
      });
}
function start_game(){
    $('#game_section').show();
    $('#welcome_section').hide();
    $('#hit_btn').show();
    $('#stand_btn').show();
    $.get( "/start", function( data ) {
        update_state(JSON.parse(data));
      });
}
function hit(){
    $.get( "hit", function( data ) {
        console.log(data)
        data = JSON.parse(data)
        console.log(data)
        if (data['result'] == undefined){
            update_state(data);
        }else{
            if (data['result']){
                alert('Победа!');
                victories+=1;
            }else{
                alert('Выиграл партье. Попробуйте ещё раз!');
            }
            $('#hit_btn').hide();
            $('#stand_btn').hide();
            update_state(JSON.parse(data['game']));
        }
      });
}
function stay(){
    $.get( "stay", function( data ) {
        console.log(data)
        data = JSON.parse(data)
        console.log(data)
        if (data['result']){
            alert('Победа!');
            victories+=1;
        }else{
            alert('Выиграл партье. Попробуйте ещё раз!');
        }
        $('#hit_btn').hide();
        $('#stand_btn').hide();
        update_state(JSON.parse(data['game']));
      });
}