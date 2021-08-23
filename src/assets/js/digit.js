
const redirectToCode = (code) => {
	window.location.assign(`/${code}`)
}
const checkCode = (code) => {
	fetch("/check", {
        method: 'POST',
        headers: {
            "Content-type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify({
            key : code,
        }),
    })
    .then(response => response.json())
    .then(json => {
		if (json.found) {
			$('#search-result').text("You are directing now.");
			redirectToCode(code)
		} else {
			$('#search-result').text("Couldn't found.");
		}
	})
}
$('.digit-group').find('input').each(function() {
	$(this).attr('maxlength', 1);
	$(this).on('keyup', function(e) {
		var parent = $($(this).parent());
		$('#search-result').html("&nbsp;");

		if(e.keyCode === 8 || e.keyCode === 37) {
			var prev = parent.find('input#' + $(this).data('previous'));
			
			if(prev.length) {
				$(prev).select();
			}
		} else if((e.keyCode >= 48 && e.keyCode <= 57) || e.keyCode === 39) {
			// (e.keyCode >= 65 && e.keyCode <= 90) || (e.keyCode >= 96 && e.keyCode <= 105)
			var next = parent.find('input#' + $(this).data('next'));
			if(next.length) {
				$(next).select();
			} else {
				if(parent.data('autosubmit')) {
					parent.submit();
				}				
				var code = ($('#digit-1').val() || "") + ($('#digit-2').val() || "") + ($('#digit-3').val() || "") + ($('#digit-4').val() || "");
				checkCode(code)
			}
		}
	});
});

const handleOneDigit = (e) => {
	if (e.value.length > e.maxLength) {
		e.value = e.value.slice(0, e.maxLength)
	};
}
