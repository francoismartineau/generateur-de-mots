function submitSection(section) {
    var elements = document.getElementById(section).children;
    data = {}
    for (const e of elements) {
        if (e.id.includes(section)) {
            const value = getValue(e);
            data[e.id.replace(section+'-', '')] = value;
        }
    }
    if (textSourceRequested(data))
        addTextSource(data);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax(
        {
            type:'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin',            
            url: '/'+section,
            data: data,
            success: (data) => {
                document.getElementById(section+'-txt').value = data;
            }
        });    
}

function getValue(element) {
    if (element.tagName === 'INPUT' && element.getAttribute('type') === 'checkbox')
        value = element.checked;
    else
        value = element.value;
    return value;
}

function textSourceRequested(data) {
    return 'mimic-text-source' in data && data['mimic-text-source'] == true;
}

function addTextSource(data) {
    const element = document.getElementById('text-source');
    const textSource = element.value;
    data['text-source'] = textSource;
}