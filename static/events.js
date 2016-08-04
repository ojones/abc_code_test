// IIFE - Immediately Invoked Function Expression
(function(yourcode) {

  // The global jQuery object is passed as a parameter
  yourcode(window.jQuery, window, document);

}(function($, window, document) {

  // The $ is now locally scoped
  var answers = []

  // Listen for the jQuery ready event on the document
  $(function() {
    // The DOM is ready!
    $('#submit').on('click', function() {
      var $answers = $('.answer')
      for (var i = $answers.length - 1; i >= 0; i -= 1) {
        $answer = $answers.eq(i)
        add_answer($answer.val(), $answer.data('id'))
      }
      post_answers(answers)
    });
  });

  // The rest of the code goes here!
  function add_answer(answer, question_id) {
    var answer = {
      "answer": answer
      , "question_id": question_id
    }
    answers.push(answer)
  }

  function submit_answers() {
    
  }
  
  function post_answers(answers) {
    var dynamicData = {};
    dynamicData["answers"] = answers;
    return $.ajax({
      url: "/complete",
      type: "post",
      data: dynamicData
    });
  }

}));