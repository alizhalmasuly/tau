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
        const route = mountainSelect?.selectedOptions[0];
        const context = {
          message: text,
          mountain: mountainSelect?.value,
          season: contextControl('season')?.value,
          duration: contextControl('duration')?.value,
          difficulty: contextControl('difficulty')?.value,
          latitude: route?.dataset.latitude,
          longitude: route?.dataset.longitude,
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