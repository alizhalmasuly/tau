(() => {
  const icons = () => window.lucide?.createIcons();
  document.addEventListener('DOMContentLoaded', () => {
    icons();
    const menuButton = document.querySelector('[data-menu-toggle]');
    const menu = document.querySelector('[data-menu]');
    menuButton?.addEventListener('click', () => {
      const open = menu.classList.toggle('is-open');
      menuButton.setAttribute('aria-expanded', String(open));
      menuButton.innerHTML = open ? '<i data-lucide="x"></i>' : '<i data-lucide="menu"></i>';
      icons();
    });
    const radios = [...document.querySelectorAll('.gear-option input')];
    const bar = document.querySelector('[data-progress-bar]');
    const label = document.querySelector('[data-progress-label]');
    const updateProgress = () => {
      if (!radios.length || !bar || !label) return;
      const groups = new Map(radios.map((radio) => [radio.name, document.querySelector(`input[name="${radio.name}"]:checked`)?.value]));
      const percentage = Math.round(([...groups.values()].filter((value) => value === 'have').length / groups.size) * 100);
      bar.style.width = `${percentage}%`; label.textContent = `${percentage}%`;
    };
    radios.forEach((radio) => radio.addEventListener('change', updateProgress)); updateProgress();
    document.querySelectorAll('[data-toast-stack] .toast').forEach((toast) => setTimeout(() => toast.remove(), 4200));

    document.querySelectorAll('[data-assistant-place-form]').forEach((searchForm) => {
      const placeInput = searchForm.querySelector('[data-assistant-mountain]');
      const status = searchForm.parentElement.querySelector('[data-assistant-place-status]');
      const button = searchForm.querySelector('button');
      const copy = {
        ru: { loading: '\u0418\u0449\u0435\u043c \u043c\u0435\u0441\u0442\u043e\u2026', found: '\u041c\u0435\u0441\u0442\u043e \u043d\u0430\u0439\u0434\u0435\u043d\u043e', empty: '\u041c\u0435\u0441\u0442\u043e \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u043e', error: '\u041f\u043e\u0438\u0441\u043a \u043d\u0435\u0434\u043e\u0441\u0442\u0443\u043f\u0435\u043d', rate: '\u041f\u043e\u0434\u043e\u0436\u0434\u0438\u0442\u0435 \u043c\u0438\u043d\u0443\u0442\u0443' },
        kk: { loading: '\u041e\u0440\u044b\u043d \u0456\u0437\u0434\u0435\u043b\u0443\u0434\u0435\u2026', found: '\u041e\u0440\u044b\u043d \u0442\u0430\u0431\u044b\u043b\u0434\u044b', empty: '\u041e\u0440\u044b\u043d \u0442\u0430\u0431\u044b\u043b\u043c\u0430\u0434\u044b', error: '\u0406\u0437\u0434\u0435\u0443 \u049b\u043e\u043b\u0436\u0435\u0442\u0456\u043c\u0441\u0456\u0437', rate: '\u0411\u0456\u0440 \u043c\u0438\u043d\u0443\u0442 \u043a\u04af\u0442\u0456\u04a3\u0456\u0437' },
        en: { loading: 'Searching…', found: 'Place found', empty: 'Place not found', error: 'Search unavailable', rate: 'Wait a minute and try again' },
      }[(document.documentElement.lang || 'en').slice(0, 2)] || { loading: 'Searching…', found: 'Place found', empty: 'Place not found', error: 'Search unavailable', rate: 'Wait a minute and try again' };
      placeInput.addEventListener('input', () => {
        delete placeInput.dataset.latitude;
        delete placeInput.dataset.longitude;
        delete placeInput.dataset.placeName;
        status.textContent = '';
      });
      searchForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const query = placeInput.value.trim();
        if (query.length < 2) return;
        button.disabled = true;
        status.textContent = copy.loading;
        try {
          const url = new URL(searchForm.dataset.endpoint, window.location.origin);
          url.searchParams.set('q', query);
          const response = await fetch(url, { headers: { Accept: 'application/json' } });
          const data = await response.json();
          const place = data.results?.[0];
          if (!response.ok) status.textContent = data.error === 'rate_limited' ? copy.rate : copy.error;
          else if (!place) status.textContent = copy.empty;
          else {
            placeInput.dataset.latitude = String(place.latitude);
            placeInput.dataset.longitude = String(place.longitude);
            placeInput.dataset.placeName = place.name;
            status.textContent = copy.found;
          }
        } catch {
          status.textContent = copy.error;
        } finally {
          button.disabled = false;
        }
      });
    });

    document.querySelectorAll('[data-chat-panel]').forEach((panel) => {
      const form = panel.querySelector('[data-chat-form]');
      const messages = panel.querySelector('[data-chat-messages]');
      const typing = panel.querySelector('[data-typing]');
      const input = panel.querySelector('[data-chat-input]');
      const csrf = form?.querySelector('[name="csrfmiddlewaretoken"]')?.value;
      const contextRoot = panel.closest('[data-assistant-root]') || panel;
      const contextControl = (name) => contextRoot.querySelector(`[data-assistant-${name}]`) || document.querySelector(`[data-assistant-${name}]`);
      const addMessage = (text, role) => {
        const message = document.createElement('div');
        message.className = `chat-message ${role === 'user' ? 'user-message' : 'assistant-message'}`;
        if (role === 'assistant') message.innerHTML = '<span class="message-avatar"><i data-lucide="mountain"></i></span>';
        const bubble = document.createElement('p');
        bubble.textContent = text;
        message.append(bubble);
        messages.append(message);
        icons();
        messages.scrollTop = messages.scrollHeight;
      };
      form?.addEventListener('submit', async (event) => {
        event.preventDefault();
        const text = input.value.trim();
        if (!text) return;
        addMessage(text, 'user');
        input.value = '';
        input.style.height = 'auto';
        typing.hidden = false;
        input.disabled = true;
        const mountainSelect = contextControl('mountain');
        const context = {
          message: text,
          mountain: mountainSelect?.dataset.placeName || mountainSelect?.value,
          season: contextControl('season')?.value,
          duration: contextControl('duration')?.value,
          difficulty: contextControl('difficulty')?.value,
          latitude: mountainSelect?.dataset.latitude,
          longitude: mountainSelect?.dataset.longitude,
        };
        try {
          const response = await fetch(panel.dataset.endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
            body: JSON.stringify(context),
          });
          const data = await response.json();
          if (!response.ok) throw new Error(data.error);
          addMessage(data.reply, 'assistant');
        } catch {
          addMessage(panel.dataset.error, 'assistant');
        } finally {
          typing.hidden = true;
          input.disabled = false;
          input.focus();
        }
      });
      input?.addEventListener('input', () => {
        input.style.height = 'auto';
        input.style.height = `${Math.min(input.scrollHeight, 110)}px`;
      });
    });

    const dockPanel = document.querySelector('[data-assistant-dock] [data-chat-panel]');
    const dockToggle = document.querySelector('[data-assistant-toggle]');
    const dockClose = document.querySelector('[data-assistant-close]');
    const setDockOpen = (open) => {
      if (!dockPanel || !dockToggle) return;
      dockPanel.hidden = !open;
      dockToggle.setAttribute('aria-expanded', String(open));
      dockToggle.setAttribute('aria-label', open ? dockToggle.dataset.closeLabel : dockToggle.dataset.openLabel);
      if (open) dockPanel.querySelector('[data-chat-input]')?.focus();
    };
    dockToggle?.addEventListener('click', () => setDockOpen(dockPanel.hidden));
    dockClose?.addEventListener('click', () => setDockOpen(false));
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && dockPanel && !dockPanel.hidden) setDockOpen(false);
    });
  });
})();
