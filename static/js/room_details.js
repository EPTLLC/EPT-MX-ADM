/*
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Room Details JavaScript
Telegram: https://t.me/EasyProTech
*/

/**
 * EPT-MX-ADM - Room Details Modal
 * Детальное модальное окно просмотра комнаты с табами
 */

console.log('room_details.js loaded');
console.log('Browser user agent:', navigator.userAgent);

let currentRoomData = null;

/**
 * Показать детальное модальное окно для комнаты
 */
function showRoomDetails(roomId) {
    console.log('showRoomDetails called with roomId:', roomId);
    console.log('Setting currentRoomData to:', { room_id: roomId });
    currentRoomData = { room_id: roomId };
    
    // Показываем модальное окно
    const modal = new bootstrap.Modal(document.getElementById('roomDetailsModal'));
    modal.show();
    console.log('Modal should be visible now');
    
    // Сбрасываем состояние табов
    resetTabs();
    
    // Загружаем базовую информацию
    loadBasicInfo(roomId);
    
    // Кнопки теперь работают через onclick атрибуты в HTML
    console.log('showRoomDetails completed');
}

/**
 * Сбросить состояние всех табов
 */
function resetTabs() {
    // Активируем первый таб
    const firstTab = document.querySelector('#basic-tab');
    const firstPanel = document.querySelector('#basic-panel');
    
    // Сбрасываем все табы
    document.querySelectorAll('.nav-link').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-pane').forEach(panel => {
        panel.classList.remove('show', 'active');
    });
    
    // Активируем первый таб
    firstTab.classList.add('active');
    firstPanel.classList.add('show', 'active');
    
    // Очищаем данные
    clearTabData();
}

/**
 * Очистить данные во всех табах
 */
function clearTabData() {
    // Основная информация
    document.getElementById('room-id-basic').textContent = '';
    document.getElementById('room-name-basic').textContent = '-';
    document.getElementById('room-topic-basic').textContent = 'Not specified';
    document.getElementById('room-alias-basic').textContent = '-';
    document.getElementById('room-creator-basic').textContent = '-';
    document.getElementById('room-created-basic').textContent = 'Unknown';
    document.getElementById('room-version-basic').textContent = '1';
    
    // Детали
    document.getElementById('room-members-details').textContent = '0';
    document.getElementById('room-local-members-details').textContent = '0';
    document.getElementById('room-local-devices').textContent = '0';
    document.getElementById('room-state-events-details').textContent = '0';
    document.getElementById('room-version-details').textContent = '1';
    
    // Таблицы
    document.getElementById('room-members-table').innerHTML = '<tr><td colspan="2" class="text-center py-3"><div class="loading"></div></td></tr>';
    document.getElementById('room-state-events-table').innerHTML = '<tr><td colspan="4" class="text-center py-3"><div class="loading"></div></td></tr>';
    document.getElementById('room-forward-extremities-table').innerHTML = '<tr><td colspan="4" class="text-center py-3"><div class="loading"></div></td></tr>';
}

/**
 * Загрузить базовую информацию о комнате
 */
async function loadBasicInfo(roomId) {
    try {
        const response = await fetch('/api/rooms/details', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ room_id: roomId })
        });
        const data = await response.json();
        
        if (data.success) {
            currentRoomData = { ...currentRoomData, ...data.room };
            displayBasicInfo(data.room);
            displayDetailsInfo(data.room);
            displayPermissionsInfo(data.room);
        } else {
            showError('Ошибка загрузки информации о комнате: ' + data.error);
        }
    } catch (error) {
        console.error('Error loading room details:', error);
        showError('Ошибка сети при загрузке информации о комнате');
    }
}

/**
 * Отобразить основную информацию
 */
function displayBasicInfo(room) {
    document.getElementById('room-id-basic').textContent = room.room_id;
    document.getElementById('room-name-basic').textContent = room.name || room.canonical_alias || 'Unnamed room';
    document.getElementById('room-topic-basic').textContent = room.topic || 'Not specified';
    document.getElementById('room-alias-basic').textContent = room.canonical_alias || '-';
    
    // Создатель с ссылкой
    const creatorElement = document.getElementById('room-creator-basic');
    if (room.creator && room.creator !== 'Unknown') {
        creatorElement.textContent = room.creator;
        creatorElement.href = `/users/${room.creator}/edit`;
        creatorElement.classList.add('text-primary');
    } else {
        creatorElement.textContent = '-';
        creatorElement.removeAttribute('href');
        creatorElement.classList.remove('text-primary');
    }
    
    // Дата создания
    if (room.creation_ts) {
        const date = new Date(room.creation_ts);
        document.getElementById('room-created-basic').textContent = date.toLocaleString();
    }
    
    document.getElementById('room-version-basic').textContent = room.room_version || '1';
}

/**
 * Отобразить детальную информацию
 */
function displayDetailsInfo(room) {
    document.getElementById('room-members-details').textContent = room.joined_members || 0;
    document.getElementById('room-local-members-details').textContent = room.local_members || 0;
    document.getElementById('room-local-devices').textContent = room.local_devices || 0;
    document.getElementById('room-state-events-details').textContent = room.state_events || 0;
    document.getElementById('room-version-details').textContent = room.room_version || '1';
    
    // Шифрование
    const encryptionElement = document.getElementById('room-encryption-details');
    if (room.encrypted) {
        encryptionElement.innerHTML = `<span class="badge bg-warning">Encrypted</span>`;
        if (room.encryption_algorithm) {
            encryptionElement.innerHTML += `<br><small class="text-muted">${room.encryption_algorithm}</small>`;
        }
    } else {
        encryptionElement.innerHTML = `<span class="badge bg-secondary">No</span>`;
    }
}

/**
 * Отобразить информацию о правах доступа
 */
function displayPermissionsInfo(room) {
    // Федерация
    document.getElementById('room-federatable-icon').textContent = room.federated ? '✅' : '❌';
    
    // В каталоге
    document.getElementById('room-in-directory-icon').textContent = room.in_directory ? '✅' : '❌';
    
    // Join rules
    document.getElementById('room-join-rules').textContent = room.join_rules || 'invite';
    
    // Guest access
    document.getElementById('room-guest-access').textContent = room.guest_access || 'can_join';
    
    // History visibility
    document.getElementById('room-history-visibility').textContent = room.history_visibility || 'shared';
}

/**
 * Загрузить список участников комнаты
 */
async function loadRoomMembers(roomId) {
    try {
        const response = await fetch('/api/rooms/members', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ room_id: roomId })
        });
        const data = await response.json();
        
        if (data.success) {
            displayMembersTable(data.members);
        } else {
            showMembersError('Ошибка загрузки участников: ' + data.error);
        }
    } catch (error) {
        console.error('Error loading room members:', error);
        showMembersError('Ошибка сети при загрузке участников');
    }
}

/**
 * Отобразить таблицу участников
 */
function displayMembersTable(members) {
    const tableBody = document.getElementById('room-members-table');
    
    if (!members || members.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="2" class="text-center py-3 text-muted">Участники не найдены</td></tr>';
        return;
    }
    
    let html = '';
    members.forEach(member => {
        html += `
            <tr>
                <td>
                    <a href="/users/${member.user_id}/edit" class="text-decoration-none text-primary">
                        ${member.user_id}
                    </a>
                </td>
                <td>${member.display_name || '-'}</td>
            </tr>
        `;
    });
    
    tableBody.innerHTML = html;
}

/**
 * Показать ошибку в таблице участников
 */
function showMembersError(message) {
    const tableBody = document.getElementById('room-members-table');
    tableBody.innerHTML = `<tr><td colspan="2" class="text-center py-3 text-danger">${message}</td></tr>`;
}

/**
 * Загрузить события состояния комнаты
 */
async function loadStateEvents(roomId) {
    try {
        const response = await fetch('/api/rooms/state_events', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ room_id: roomId })
        });
        const data = await response.json();
        
        if (data.success) {
            displayStateEventsTable(data.events);
        } else {
            showStateEventsError('Ошибка загрузки событий: ' + data.error);
        }
    } catch (error) {
        console.error('Error loading state events:', error);
        showStateEventsError('Ошибка сети при загрузке событий');
    }
}

/**
 * Отобразить таблицу событий состояния
 */
function displayStateEventsTable(events) {
    const tableBody = document.getElementById('room-state-events-table');
    
    if (!events || events.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="4" class="text-center py-3 text-muted">События не найдены</td></tr>';
        return;
    }
    
    let html = '';
    events.forEach(event => {
        const date = new Date(event.origin_server_ts || event.timestamp);
        html += `
            <tr>
                <td><code class="small">${event.type}</code></td>
                <td>${date.toLocaleString()}</td>
                <td><span class="badge bg-secondary">object Object</span></td>
                <td>
                    <a href="/users/${event.sender}/edit" class="text-decoration-none text-primary">
                        ${event.sender}
                    </a>
                </td>
            </tr>
        `;
    });
    
    tableBody.innerHTML = html;
}

/**
 * Показать ошибку в таблице событий
 */
function showStateEventsError(message) {
    const tableBody = document.getElementById('room-state-events-table');
    tableBody.innerHTML = `<tr><td colspan="4" class="text-center py-3 text-danger">${message}</td></tr>`;
}

/**
 * Загрузить forward extremities
 */
async function loadForwardExtremities(roomId) {
    try {
        const response = await fetch(`/api/rooms/${roomId}/forward_extremities`);
        const data = await response.json();
        
        if (data.success) {
            displayForwardExtremitiesTable(data.extremities);
        } else {
            showForwardExtremitiesError('Ошибка загрузки: ' + data.error);
        }
    } catch (error) {
        console.error('Error loading forward extremities:', error);
        showForwardExtremitiesError('Ошибка сети при загрузке');
    }
}

/**
 * Отобразить таблицу forward extremities
 */
function displayForwardExtremitiesTable(extremities) {
    const tableBody = document.getElementById('room-forward-extremities-table');
    
    if (!extremities || extremities.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="4" class="text-center py-3 text-muted">Forward extremities не найдены</td></tr>';
        return;
    }
    
    let html = '';
    extremities.forEach(ext => {
        const date = new Date(ext.timestamp);
        html += `
            <tr>
                <td><code class="small">${ext.event_id}</code></td>
                <td>${date.toLocaleString()}</td>
                <td>${ext.depth || '-'}</td>
                <td>${ext.state_group || '-'}</td>
            </tr>
        `;
    });
    
    tableBody.innerHTML = html;
}

/**
 * Показать ошибку в таблице forward extremities
 */
function showForwardExtremitiesError(message) {
    const tableBody = document.getElementById('room-forward-extremities-table');
    tableBody.innerHTML = `<tr><td colspan="4" class="text-center py-3 text-danger">${message}</td></tr>`;
}

/**
 * Показать общую ошибку
 */
function showError(message) {
    console.error(message);
    // Можно добавить показ toast уведомления
}



/**
 * Подтверждение удаления комнаты
 */
function deleteRoomConfirm(roomId) {
    console.log('deleteRoomConfirm called with roomId:', roomId);
    const roomName = currentRoomData.name || currentRoomData.canonical_alias || roomId;
    
    if (confirm(`Вы уверены, что хотите удалить комнату "${roomName}"?\n\nЭто навсегда удалит комнату и все её данные.\nЭто действие нельзя отменить!`)) {
        deleteRoom(roomId);
    }
}



/**
 * Удалить комнату
 */
async function deleteRoom(roomId) {
    console.log('deleteRoom called with roomId:', roomId);
    try {
        const response = await fetch('/api/rooms/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                room_id: roomId,
                message: 'Room deleted by administrator'
            })
        });
        
        // Check if response is JSON
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error('Server returned non-JSON response. You may need to log in again.');
        }
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            alert('Комната успешно удалена');
            // Закрываем модальное окно
            const modal = bootstrap.Modal.getInstance(document.getElementById('roomDetailsModal'));
            if (modal) modal.hide();
            // Обновляем список комнат если нужно
            if (typeof refreshRoomsList === 'function') {
                refreshRoomsList();
            } else {
                window.location.reload();
            }
        } else {
            alert('Ошибка удаления комнаты: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error deleting room:', error);
        alert('Ошибка при удалении комнаты: ' + error.message);
    }
}

/**
 * Привязать обработчики кнопок модального окна
 */
function bindModalButtons() {
    console.log('Modal buttons are now using onclick attributes');
    // Удаляем эту функцию, так как теперь используем onclick атрибуты в HTML
}

/**
 * Обработчики событий табов
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded fired in room_details.js');
    
    // Обработчики переключения табов
    const membersTab = document.getElementById('members-tab');
    const stateEventsTab = document.getElementById('state-events-tab');
    const forwardExtremitiesTab = document.getElementById('forward-extremities-tab');
    const editBtn = document.getElementById('editRoomBtn');
    
    if (membersTab) {
        membersTab.addEventListener('click', function() {
            if (currentRoomData && currentRoomData.room_id) {
                loadRoomMembers(currentRoomData.room_id);
            }
        });
    }
    
    if (stateEventsTab) {
        stateEventsTab.addEventListener('click', function() {
            if (currentRoomData && currentRoomData.room_id) {
                loadStateEvents(currentRoomData.room_id);
            }
        });
    }
    
    if (forwardExtremitiesTab) {
        forwardExtremitiesTab.addEventListener('click', function() {
            if (currentRoomData && currentRoomData.room_id) {
                loadForwardExtremities(currentRoomData.room_id);
            }
        });
    }
    
    // Кнопка редактирования
    if (editBtn) {
        editBtn.addEventListener('click', function() {
            console.log('editRoomBtn clicked, currentRoomData:', currentRoomData);
            if (currentRoomData && currentRoomData.room_id) {
                window.location.href = `/rooms/${currentRoomData.room_id}/edit`;
            }
        });
    } else {
        console.log('editRoomBtn not found in DOM');
    }
    
    // Clear и Delete кнопки теперь используют onclick атрибуты в HTML
});



/**
 * Действие удаления комнаты (вызывается через onclick)
 */
function deleteRoomAction() {
    console.log('=== deleteRoomAction START ===');
    console.log('deleteRoomAction called, currentRoomData:', currentRoomData);
    console.log('typeof currentRoomData:', typeof currentRoomData);
    console.log('currentRoomData is null?', currentRoomData === null);
    console.log('currentRoomData is undefined?', currentRoomData === undefined);
    
    if (currentRoomData && currentRoomData.room_id) {
        const roomName = currentRoomData.name || currentRoomData.canonical_alias || currentRoomData.room_id;
        console.log('Room name for confirmation:', roomName);
        
        console.log('Showing confirmation dialog...');
        if (confirm(`Вы уверены, что хотите удалить комнату "${roomName}"?\n\nЭто навсегда удалит комнату и все её данные.\nЭто действие нельзя отменить!`)) {
            console.log('User confirmed delete action, calling deleteRoom()');
            deleteRoom(currentRoomData.room_id);
        } else {
            console.log('User cancelled delete action');
        }
    } else {
        console.log('ERROR: No currentRoomData available for delete action');
        console.log('currentRoomData value:', currentRoomData);
        alert('Данные комнаты не загружены. Попробуйте открыть модальное окно заново.');
    }
    console.log('=== deleteRoomAction END ===');
}

/**
 * Действие разблокировки комнаты (вызывается через onclick)
 */
function unblockRoomAction() {
    console.log('unblockRoomAction called, currentRoomData:', currentRoomData);
    
    if (currentRoomData && currentRoomData.room_id) {
        const roomName = currentRoomData.name || currentRoomData.canonical_alias || currentRoomData.room_id;
        
        if (confirm(`Are you sure you want to unblock room "${roomName}"?`)) {
            unblockRoom(currentRoomData.room_id);
        }
    } else {
        alert('Room data not loaded. Please reopen the modal window.');
    }
}

/**
 * Разблокировать комнату
 */
async function unblockRoom(roomId) {
    try {
        const response = await fetch('/api/rooms/unblock', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ room_id: roomId })
        });
        
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error('Server returned non-JSON response. You may need to log in again.');
        }
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            alert('Room unblocked successfully');
            // Можно обновить статус в UI если нужно
        } else {
            alert('Error unblocking room: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error unblocking room:', error);
        alert('Error unblocking room: ' + error.message);
    }
}

/**
 * Действие назначения админа комнаты (вызывается через onclick)
 */
function makeRoomAdminAction() {
    console.log('makeRoomAdminAction called, currentRoomData:', currentRoomData);
    
    if (currentRoomData && currentRoomData.room_id) {
        const userId = prompt('Enter User ID to make room admin:');
        if (userId && userId.trim()) {
            makeRoomAdmin(currentRoomData.room_id, userId.trim());
        }
    } else {
        alert('Room data not loaded. Please reopen the modal window.');
    }
}

/**
 * Назначить админа комнаты
 */
async function makeRoomAdmin(roomId, userId) {
    try {
        const response = await fetch('/api/rooms/make_admin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                room_id: roomId,
                user_id: userId
            })
        });
        
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error('Server returned non-JSON response. You may need to log in again.');
        }
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            alert('User made room admin successfully');
            // Можно обновить список участников если нужно
            if (currentRoomData && currentRoomData.room_id) {
                loadRoomMembers(currentRoomData.room_id);
            }
        } else {
            alert('Error making room admin: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error making room admin:', error);
        alert('Error making room admin: ' + error.message);
    }
}

/**
 * Экспорт функций для использования в templates
 */
console.log('Exporting functions to window object...');
window.showRoomDetails = showRoomDetails;
window.deleteRoomAction = deleteRoomAction;
window.unblockRoomAction = unblockRoomAction;
window.makeRoomAdminAction = makeRoomAdminAction;
console.log('Functions exported to window:');
console.log('- window.showRoomDetails:', typeof window.showRoomDetails);
console.log('- window.deleteRoomAction:', typeof window.deleteRoomAction);
console.log('- window.unblockRoomAction:', typeof window.unblockRoomAction);
console.log('- window.makeRoomAdminAction:', typeof window.makeRoomAdminAction); 