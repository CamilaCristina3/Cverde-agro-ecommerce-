console.log("Cverde frontend assets loaded");

document.addEventListener('DOMContentLoaded', () => {
  const sliders = document.querySelectorAll('.featured-slider-wrapper');
  sliders.forEach(wrapper => {
    const slider = wrapper.querySelector('.featured-slider');
    const prev = wrapper.querySelector('.slider-prev');
    const next = wrapper.querySelector('.slider-next');

    if (!slider || !prev || !next) return;

    const scrollAmount = slider.offsetWidth * 0.75;

    prev.addEventListener('click', () => {
      slider.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });

    next.addEventListener('click', () => {
      slider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });
  });
});
