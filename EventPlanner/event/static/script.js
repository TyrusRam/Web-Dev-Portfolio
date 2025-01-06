
function checkScreenSize(){
    const mobile = document.getElementById('mobile-nav');
    const eventContainer = document.getElementById('event-container');
    const mobileEventContainer = document.getElementById('mobile-event-container');

    if (window.innerWidth >= 481){
        mobile.classList.remove('active');
        eventContainer.style.display = 'flex';
        mobileEventContainer.style.display = 'none';
    }else if (window.innerWidth <= 480){
        eventContainer.style.display = 'none'
        mobileEventContainer.style.display = 'block';
    }
                
}
addEventListener("DOMContentLoaded", ()=> {
    const hamb = document.getElementById('hamburger');
    const mobile = document.getElementById('mobile-nav');
    const categorylabels = document.querySelectorAll('.category-label');
    const discovForm = document.getElementById('category-form');
    const sample = document.getElementsByClassName
    const discoverContainer = document.getElementById('discover-container');
    const eventContainer = document.getElementById('event-container');
    const mobileEventContainer = document.getElementById('mobile-event-container');
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const rsvpButton = document.getElementById('rsvp-button');
    

    hamb.addEventListener('click', ()=> {
        mobile.classList.toggle('active');
    })

    categorylabels.forEach(item => {
        item.addEventListener('click', ()=> {    
            const seltectedCategory = item.getAttribute('data-category');        
            const data = {                
                category: seltectedCategory                
            };                
            fetch(`/discover`, {                
                method: 'POST',                
                headers: {                                
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}',
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('network response was not ok.');
            })
            .then(data => {
                const events = data.events;
                discoverContainer.style.display = 'none';
                if (window.innerWidth >= 481){
                    eventContainer.style.display = 'flex';
                    mobileEventContainer.style.display = 'none';
                }else if (window.innerWidth <= 480){
                    eventContainer.style.display = 'none';
                    mobileEventContainer.style.display = 'block';
                }
                            
                eventContainer.innerHTML = '';
                mobileEventContainer.innerHTML = '';

                events.forEach(event => {
                    const eventElement = document.createElement('div');
                    eventElement.classList.add('event-item');
                    const mobileEventElement = document.createElement('div');
                    mobileEventElement.classList.add('mobile-event-item');
                    const startDate = new Date(event.start_date).toLocaleDateString('en-US',{
                        year: 'numeric',
                        month: '2-digit',
                        day: '2-digit'
                    });

                    const [hours, minutes] = event.start_time.split(':');
                                
                    const startTime = new Date(0, 0, 0, hours, minutes).toLocaleTimeString('en-US',{
                        hour: 'numeric',
                        minute: '2-digit',
                        hour12: true
                    });
                                
                    const rsvpDeadlineDate = new Date(event.RSVP_deadline).toLocaleDateString('en-US',{
                        year: 'numeric',
                        month: '2-digit',
                        day: '2-digit'
                    });

                    const rsvpDeadlineTime = new Date(event.RSVP_deadline).toLocaleTimeString('en-US',{
                        hour: 'numeric',
                        minute: '2-digit',
                        hour12: true
                    });

                    eventElement.innerHTML = `
                        <h1>${event.title}</h1>
                        <p>${event.category}</p>
                        <p>Start Date: ${startDate}</p>
                        <p>Start Time: ${startTime}</p>
                        <p>Deadline: ${rsvpDeadlineDate} ${rsvpDeadlineTime}</p>
                        <hr>
                    `;
                                
                    mobileEventElement.innerHTML = `
                        <h3>${event.title}</h3>
                        <p>${event.category}</p>
                        <p>Start Date: ${startDate}</p>
                        <p>Start Time: ${startTime}</p>
                        <p>Deadline: ${rsvpDeadlineDate} ${rsvpDeadlineTime}</p>
                        <hr>
                    `;

                    eventContainer.appendChild(eventElement);
                    mobileEventContainer.appendChild(mobileEventElement);
                                
                    eventElement.addEventListener('click', () => {
                        const event_id = event.id;
                        window.location.href = `/event/${event_id}`;
                    })
                                
                    mobileEventContainer.addEventListener('click', () => {
                        const event_id = event.id;
                        window.location.href = `/event/${event_id}`;
                    })
         
                });                   
                        
            })
                        
                        
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            })
           
        })
                
    })

    if (rsvpButton){ 
        const eventIdRsvp = rsvpButton.getAttribute("data-event-id");
        const csrfTokenRsvp = rsvpButton.getAttribute("data-csrf-token");

        rsvpButton.addEventListener('click', () => {
            
            const data = { 
                event_id: eventIdRsvp, 
                
            };
                            

            fetch('/rsvp/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfTokenRsvp,
                },

                body: JSON.stringify(data),
                                
            })
            .then(response => {
                if (response.ok) {
                    rsvpButton.disabled = true;
                } else {
                    console.error('rsvp failed');
                }
            })
            .catch(error => console.error('Error: ', error));
        })
    }
            
});

            
window.addEventListener('resize', checkScreenSize);
