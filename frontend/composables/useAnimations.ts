import { gsap } from 'gsap'
import { onMounted, onUnmounted, ref } from 'vue'

export function useAnimations() {
  const isAnimated = ref(false)

  const fadeIn = (element: HTMLElement, duration = 0.5, delay = 0) => {
    gsap.fromTo(element, 
      { opacity: 0, y: 20 },
      { opacity: 1, y: 0, duration, delay, ease: 'power2.out' }
    )
  }

  const slideIn = (element: HTMLElement, direction = 'left', duration = 0.5, delay = 0) => {
    const x = direction === 'left' ? -50 : direction === 'right' ? 50 : 0
    const y = direction === 'up' ? 50 : direction === 'down' ? -50 : 0
    
    gsap.fromTo(element,
      { opacity: 0, x, y },
      { opacity: 1, x: 0, y: 0, duration, delay, ease: 'power2.out' }
    )
  }

  const scaleIn = (element: HTMLElement, duration = 0.5, delay = 0) => {
    gsap.fromTo(element,
      { opacity: 0, scale: 0.8 },
      { opacity: 1, scale: 1, duration, delay, ease: 'back.out(1.7)' }
    )
  }

  const staggerIn = (elements: HTMLElement[], duration = 0.4, stagger = 0.1) => {
    gsap.fromTo(elements,
      { opacity: 0, y: 30 },
      { opacity: 1, y: 0, duration, stagger, ease: 'power2.out' }
    )
  }

  const pulse = (element: HTMLElement, duration = 0.5) => {
    gsap.to(element, {
      scale: 1.05,
      duration: duration / 2,
      yoyo: true,
      repeat: 1,
      ease: 'power1.inOut'
    })
  }

  const bounce = (element: HTMLElement) => {
    gsap.to(element, {
      y: -10,
      duration: 0.3,
      yoyo: true,
      repeat: 1,
      ease: 'power2.out'
    })
  }

  const shimmer = (element: HTMLElement) => {
    gsap.fromTo(element,
      { backgroundPosition: '-200% 0' },
      { backgroundPosition: '200% 0', duration: 1.5, ease: 'none' }
    )
  }

  const countUp = (element: HTMLElement, target: number, duration = 2) => {
    gsap.to({ value: 0 }, {
      value: target,
      duration,
      ease: 'power2.out',
      onUpdate: function() {
        element.textContent = Math.round(this.targets()[0].value).toLocaleString()
      }
    })
  }

  const hoverEffect = (element: HTMLElement, scale = 1.05) => {
    element.addEventListener('mouseenter', () => {
      gsap.to(element, { scale, duration: 0.3, ease: 'power2.out' })
    })
    element.addEventListener('mouseleave', () => {
      gsap.to(element, { scale: 1, duration: 0.3, ease: 'power2.out' })
    })
  }

  const cardEnter = (element: HTMLElement) => {
    gsap.fromTo(element,
      { opacity: 0, y: 40, scale: 0.95 },
      { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: 'power3.out' }
    )
  }

  const animateOnScroll = (elements: HTMLElement[]) => {
    elements.forEach((element, index) => {
      gsap.fromTo(element,
        { opacity: 0, y: 50 },
        {
          opacity: 1,
          y: 0,
          duration: 0.6,
          delay: index * 0.1,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: element,
            start: 'top 80%',
            toggleActions: 'play none none reverse'
          }
        }
      )
    })
  }

  const loadingAnimation = (element: HTMLElement) => {
    gsap.fromTo(element,
      { rotation: 0 },
      { rotation: 360, duration: 1, repeat: -1, ease: 'none' }
    )
  }

  const successAnimation = (element: HTMLElement) => {
    gsap.fromTo(element,
      { scale: 0, opacity: 0 },
      { scale: 1, opacity: 1, duration: 0.5, ease: 'elastic.out(1, 0.5)' }
    )
  }

  const errorShake = (element: HTMLElement) => {
    gsap.to(element, {
      x: [-10, 10, -10, 10, -5, 5, 0],
      duration: 0.5,
      ease: 'power2.inOut'
    })
  }

  return {
    isAnimated,
    fadeIn,
    slideIn,
    scaleIn,
    staggerIn,
    pulse,
    bounce,
    shimmer,
    countUp,
    hoverEffect,
    cardEnter,
    animateOnScroll,
    loadingAnimation,
    successAnimation,
    errorShake
  }
}
