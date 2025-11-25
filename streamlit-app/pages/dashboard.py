import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from api.backend_client import BackendClient
import pandas as pd
import json


st.set_page_config(page_title="Dashboard", layout="wide")


# Initialize cookies
cookies = EncryptedCookieManager(
    prefix="myapp_",
    password="987@%#@#958"
)


if not cookies.ready():
    st.stop()


# Restore session
if "token" not in st.session_state or st.session_state.token is None:
    if cookies.get("token"):
        st.session_state.token = cookies["token"]
        st.session_state.user = {"username": cookies.get("username", "User")}
    else:
        st.error("🔒 Please login first")
        st.markdown('<meta http-equiv="refresh" content="0; url=/" />', unsafe_allow_html=True)
        st.stop()


# Sidebar
with st.sidebar:
    st.write(f"**Logged in as:**")
    st.write(f"👤 {st.session_state.user['username']}")
    
    st.write("---")
    
    if st.button("🚪 Logout", width="stretch"):
        st.session_state.token = None
        st.session_state.user = None
        cookies["token"] = ""
        cookies["username"] = ""
        cookies.save()
        st.success("Logged out!")
        st.markdown('<meta http-equiv="refresh" content="1; url=/" />', unsafe_allow_html=True)
        st.stop()


# Main content
st.subheader("Dashboard")


# Fetch ALL data from backend
with st.spinner("Loading dashboard data..."):
    client = BackendClient()
    data, status = client.get_dashboard_data(st.session_state.token)


if status == 200 and data.get("data"):
    dashboard_items = data["data"]
    
    if len(dashboard_items) > 0:
        # Define columns to show and edit
        SHOW_COLUMNS = [
            "WhatsApp Status",
            "Review Status",
            "Blocked Date",
            "No of Days",
            "Unblocked Date",
            "Recharge Date",
        ]
        
        # Filter data to show only these columns + id
        filtered_items = []
        for item in dashboard_items:
            filtered_item = {'id': item['id'], 'Number':item['Number']}  # Keep id for updates
            for col in SHOW_COLUMNS:
                if col in item:
                    filtered_item[col] = item[col]
            filtered_items.append(filtered_item)
        
        # Convert to JSON for JavaScript
        data_json = json.dumps(filtered_items)
        editable_json = json.dumps(SHOW_COLUMNS)
        backend_url = "http://localhost:5000"  # Update for production
        token = st.session_state.token
        
        # HTML Component
        html_component = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                * {{
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }}
                
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    padding: 20px;
                    background: #f8f9fa;
                }}
                
                .controls {{
                    background: white;
                    padding: 15px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                
                .controls-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 10px;
                }}
                
                .controls label {{
                    font-weight: 600;
                    color: #333;
                }}
                
                .column-selector {{
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
                }}
                
                .column-checkbox {{
                    display: flex;
                    align-items: center;
                    gap: 5px;
                    padding: 8px 12px;
                    background: #f1f3f5;
                    border-radius: 6px;
                    cursor: pointer;
                    transition: all 0.2s;
                    user-select: none;
                }}
                
                .column-checkbox:hover {{
                    background: #e9ecef;
                }}
                
                .column-checkbox.checked {{
                    background: #d3f9d8;
                    border: 2px solid #37b24d;
                }}
                
                .column-checkbox input {{
                    cursor: pointer;
                    width: 18px;
                    height: 18px;
                }}
                
                .selected-count {{
                    background: #339af0;
                    color: white;
                    padding: 4px 12px;
                    border-radius: 20px;
                    font-size: 13px;
                    font-weight: 600;
                }}
                
                .table-container {{
                    overflow-x: auto;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                
                table {{
                    width: 100%;
                    min-width: 800px;
                    border-collapse: collapse;
                }}
                
                th {{
                    background: #f8f9fa;
                    padding: 12px 10px;
                    text-align: left;
                    font-weight: 600;
                    border-bottom: 2px solid #dee2e6;
                    white-space: nowrap;
                    position: sticky;
                    top: 0;
                    z-index: 10;
                }}
                
                td {{
                    padding: 10px;
                    border-bottom: 1px solid #dee2e6;
                    white-space: nowrap;
                }}
                
                tr:hover:not(.editing) {{
                    background: #f8f9fa;
                }}
                
                tr.editing {{
                    background: #fff3cd !important;
                }}
                
                .edit-input {{
                    width: 100%;
                    min-width: 120px;
                    padding: 6px 8px;
                    border: 2px solid #0066cc;
                    border-radius: 4px;
                    font-size: 14px;
                    background: white;
                }}
                
                .edit-input[type="date"] {{
                    padding: 6px 8px;
                    cursor: pointer;
                }}
                
                .btn {{
                    padding: 6px 12px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 13px;
                    font-weight: 500;
                    transition: all 0.2s;
                    white-space: nowrap;
                }}
                
                .btn:disabled {{
                    opacity: 0.5;
                    cursor: not-allowed;
                }}
                
                .btn-edit {{
                    background: #0066cc;
                    color: white;
                }}
                
                .btn-edit:hover:not(:disabled) {{
                    background: #0052a3;
                }}
                
                .btn-update {{
                    background: #28a745;
                    color: white;
                    margin-right: 5px;
                }}
                
                .btn-update:hover {{
                    background: #218838;
                }}
                
                .btn-cancel {{
                    background: #dc3545;
                    color: white;
                }}
                
                .btn-cancel:hover {{
                    background: #c82333;
                }}
                
                .message {{
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    padding: 12px 20px;
                    border-radius: 6px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    z-index: 1000;
                    animation: slideIn 0.3s ease;
                }}
                
                @keyframes slideIn {{
                    from {{ transform: translateX(400px); opacity: 0; }}
                    to {{ transform: translateX(0); opacity: 1; }}
                }}
                
                .message.success {{
                    background: #d4edda;
                    color: #155724;
                    border: 1px solid #c3e6cb;
                }}
                
                .message.error {{
                    background: #f8d7da;
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                }}
            </style>
        </head>
        <body>
            <div class="controls">
                <div class="controls-header">
                    <label>📝 Select Columns to Edit:</label>
                    <span class="selected-count" id="selectedCount">0 selected</span>
                </div>
                <div class="column-selector" id="columnSelector"></div>
            </div>
            
            <div class="table-container">
                <table id="dataTable">
                    <thead id="tableHeader"></thead>
                    <tbody id="tableBody"></tbody>
                </table>
            </div>
            
            <script>
                console.log('🚀 Script started');
                
                const data = {data_json};
                const editableColumns = {editable_json};
                const backendUrl = '{backend_url}';
                const token = '{token}';
                
                let selectedColumns = [];
                let editingRowId = null;
                
                // Define which columns are date columns
                const DATE_COLUMNS = Object.keys(data[0]).filter(col => 
                    col.includes('Date')
                );
                
                console.log('📊 Data loaded:', data.length, 'rows');
                console.log('✏️ Columns:', editableColumns);
                console.log('📅 Date columns:', DATE_COLUMNS);

                function isDateColumn(columnName) {{
                    return DATE_COLUMNS.includes(columnName);
                }}

                // ✅ NEW: Calculate days between two dates
                function calculateDays(blockedDateStr) {{
                    if (!blockedDateStr || blockedDateStr === "NA" || blockedDateStr === "") {{
                        return "NA";
                    }}
                    
                    try {{
                        const today = new Date();
                        const blockedDate = new Date(blockedDateStr);
                        
                        // Check if date is valid
                        if (isNaN(blockedDate.getTime())) {{
                            return "NA";
                        }}
                        
                        // Set time to 0 for accurate day calculation
                        today.setHours(0, 0, 0, 0);
                        blockedDate.setHours(0, 0, 0, 0);
                        
                        // Calculate difference in milliseconds
                        const diffMs = today.getTime() - blockedDate.getTime();
                        
                        // Convert to days
                        const diffDays = Math.floor(diffMs / (1000 * 3600 * 24)) + 1;
                        
                        return diffDays > 0 ? diffDays.toString() : "1";
                    }} catch (error) {{
                        console.error('Error calculating days:', error);
                        return "NA";
                    }}
                }}
                
                // Initialize
                function init() {{
                    createColumnSelector();
                    renderTable();
                    updateSelectedCount();
                    console.log('✅ Initialization complete');
                }}
                
                // Create column selector checkboxes
                function createColumnSelector() {{
                    const selector = document.getElementById('columnSelector');
                    
                    editableColumns.forEach(col => {{
                        // Skip "No of Days" - it's auto-calculated
                        if (col === "No of Days") {{
                            return;
                        }}
                        
                        const label = document.createElement('label');
                        label.className = 'column-checkbox';
                        label.setAttribute('data-column', col);
                        
                        const checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.value = col;
                        checkbox.id = 'check_' + col.replace(/\\s+/g, '_');
                        
                        const span = document.createElement('span');
                        span.textContent = col;
                        
                        label.appendChild(checkbox);
                        label.appendChild(span);
                        
                        label.addEventListener('click', function(e) {{
                            if (e.target === checkbox) return;
                            checkbox.checked = !checkbox.checked;
                            toggleColumn(checkbox);
                        }});
                        
                        checkbox.addEventListener('change', function() {{
                            toggleColumn(this);
                        }});
                        
                        selector.appendChild(label);
                    }});
                    
                    console.log('✅ Column selector created');
                }}
                
                // Toggle column selection
                function toggleColumn(checkbox) {{
                    const col = checkbox.value;
                    const label = checkbox.closest('.column-checkbox');
                    
                    if (checkbox.checked) {{
                        if (!selectedColumns.includes(col)) {{
                            selectedColumns.push(col);
                            label.classList.add('checked');
                            console.log('✅ Added:', col);
                        }}
                    }} else {{
                        selectedColumns = selectedColumns.filter(c => c !== col);
                        label.classList.remove('checked');
                        console.log('❌ Removed:', col);
                    }}
                    
                    updateSelectedCount();
                    renderTable();
                    
                    console.log('📋 Current selection:', selectedColumns);
                }}
                
                // Update selected count display
                function updateSelectedCount() {{
                    const count = selectedColumns.length;
                    const countEl = document.getElementById('selectedCount');
                    countEl.textContent = count + ' selected';
                    countEl.style.display = count > 0 ? 'inline-block' : 'none';
                }}
                
                // Render table
                function renderTable() {{
                    const columns = Object.keys(data[0]);
                    
                    // Header
                    const header = document.getElementById('tableHeader');
                    header.innerHTML = '<tr>' + 
                        columns.map(col => '<th>' + col + '</th>').join('') +
                        '<th>Actions</th></tr>';
                    
                    // Body
                    const tbody = document.getElementById('tableBody');
                    tbody.innerHTML = '';
                    
                    data.forEach(row => {{
                        const tr = document.createElement('tr');
                        const isEditing = editingRowId === row.id;
                        
                        if (isEditing) {{
                            tr.className = 'editing';
                        }}
                        
                        // Data columns
                        columns.forEach(col => {{
                            const td = document.createElement('td');
                            let displayValue = row[col] || '';
                            
                            // ✅ Special logic for No of Days column
                            if (col === "No of Days") {{
                                // Auto-calculate based on Blocked Date
                                const blockedDateStr = row["Blocked Date"];
                                displayValue = calculateDays(blockedDateStr);
                                console.log('📅 Calculating days for:', blockedDateStr, '= ', displayValue);
                            }}
                            
                            const isEditable = isEditing && selectedColumns.includes(col) && col !== "No of Days";
                            
                            if (isEditable) {{
                                const input = document.createElement('input');
                                
                                if (isDateColumn(col)) {{
                                    input.type = 'date';
                                    // Restrict selection to today and earlier
                                    const today = new Date();
                                    const yyyy = today.getFullYear();
                                    const mm = String(today.getMonth() + 1).padStart(2, '0');
                                    const dd = String(today.getDate()).padStart(2, '0');
                                    input.max = yyyy + '-' + mm + '-' + dd;
                                }} else {{
                                    input.type = 'text';
                                }}
                                
                                input.className = 'edit-input';
                                input.value = row[col] || '';
                                input.setAttribute('data-column', col);
                                input.setAttribute('data-row-id', row.id);
                                td.appendChild(input);
                            }} else {{
                                td.textContent = displayValue;
                            }}
                            
                            tr.appendChild(td);
                        }});
                        
                        // Actions column
                        const actionTd = document.createElement('td');
                        
                        if (isEditing) {{
                            const updateBtn = document.createElement('button');
                            updateBtn.className = 'btn btn-update';
                            updateBtn.textContent = '💾 Update';
                            updateBtn.onclick = function() {{ updateRow(row.id); }};
                            
                            const cancelBtn = document.createElement('button');
                            cancelBtn.className = 'btn btn-cancel';
                            cancelBtn.textContent = '❌ Cancel';
                            cancelBtn.onclick = cancelEdit;
                            
                            actionTd.appendChild(updateBtn);
                            actionTd.appendChild(cancelBtn);
                        }} else {{
                            const editBtn = document.createElement('button');
                            editBtn.className = 'btn btn-edit';
                            editBtn.textContent = '✏️ Edit';
                            editBtn.disabled = selectedColumns.length === 0;
                            editBtn.title = selectedColumns.length === 0 ? 'Select columns first' : 'Edit this row';
                            editBtn.onclick = function() {{ editRow(row.id); }};
                            
                            actionTd.appendChild(editBtn);
                        }}
                        
                        tr.appendChild(actionTd);
                        tbody.appendChild(tr);
                    }});
                }}
                
                // Edit row
                function editRow(rowId) {{
                    console.log('🔧 Edit clicked for row:', rowId);
                    
                    if (selectedColumns.length === 0) {{
                        showMessage('⚠️ Please select at least one column to edit', 'error');
                        return;
                    }}
                    
                    editingRowId = rowId;
                    renderTable();
                    console.log('✅ Now editing row:', rowId);
                }}
                
                // Cancel edit
                function cancelEdit() {{
                    console.log('❌ Edit cancelled');
                    editingRowId = null;
                    renderTable();
                }}
                
                // Update row
                async function updateRow(rowId) {{
                    console.log('💾 Updating row:', rowId);
                    
                    const inputs = document.querySelectorAll('input[data-row-id="' + rowId + '"]');
                    const updatedData = {{}};
                    
                    inputs.forEach(input => {{
                        const colName = input.getAttribute('data-column');
                        updatedData[colName] = input.value;
                        console.log('  📝', colName, '=', input.value);
                    }});
                    
                    if ("Blocked Date" in updatedData) {{
                        updatedData["No of Days"] = calculateDays(updatedData["Blocked Date"]);
                    }}  

                    if ("Unblocked Date" in updatedData && updatedData["Unblocked Date"] && updatedData["Unblocked Date"] !== "NA") {{
                        updatedData["Blocked Date"] = "NA";
                        updatedData["No of Days"] = "NA";
                        console.log('Unblocked Date set, resetting Blocked Date and No of Days to NA');
                    }}

                    console.log('📤 Sending update:', updatedData);
                    
                    try {{
                        const url = backendUrl + '/api/dashboard/' + rowId;
                        console.log('🌐 PUT to:', url);
                        
                        const response = await fetch(url, {{
                            method: 'PUT',
                            headers: {{
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer ' + token
                            }},
                            body: JSON.stringify(updatedData)
                        }});
                        
                        console.log('📥 Response status:', response.status);
                        
                        if (response.ok) {{
                            const responseData = await response.json();
                            console.log('✅ Update successful:', responseData);
                            
                            // Update local data
                            const rowIndex = data.findIndex(r => r.id === rowId);
                            data[rowIndex] = {{ ...data[rowIndex], ...updatedData }};
                            
                            showMessage('✅ Updated successfully!', 'success');
                            editingRowId = null;
                            renderTable();
                        }} else {{
                            const errorData = await response.json();
                            console.error('❌ Update failed:', errorData);
                            showMessage('❌ Update failed: ' + (errorData.message || 'Unknown error'), 'error');
                        }}
                    }} catch (error) {{
                        console.error('❌ Network error:', error);
                        showMessage('❌ Network error: ' + error.message, 'error');
                    }}
                }}
                
                // Show message
                function showMessage(text, type) {{
                    const msg = document.createElement('div');
                    msg.className = 'message ' + type;
                    msg.textContent = text;
                    document.body.appendChild(msg);
                    
                    setTimeout(function() {{
                        msg.remove();
                    }}, 3000);
                }}
                
                // Initialize on load
                init();
            </script>
        </body>
        </html>
        """
        
        # Display HTML component
        st.components.v1.html(html_component, height=800, scrolling=True)
        
        st.write("---")
        
        # Download CSV with calculated No of Days
        csv_items = []
        for item in filtered_items:
            csv_item = item.copy()
            # Calculate No of Days for CSV export
            blocked_date = item.get('Blocked Date', 'NA')
            if blocked_date and blocked_date != 'NA':
                try:
                    from datetime import datetime
                    today = datetime.now()
                    blocked_date_obj = datetime.strptime(blocked_date, '%Y-%m-%d')
                    days_diff = (today - blocked_date_obj).days + 1
                    csv_item['No of Days'] = max(1, days_diff)
                except:
                    csv_item['No of Days'] = 'NA'
            else:
                csv_item['No of Days'] = 'NA'
            csv_items.append(csv_item)
        
        df = pd.DataFrame(csv_items)
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="dashboard_data.csv",
            mime="text/csv"
        )
        
    else:
        st.info("No data available.")
        
elif status == 401:
    st.error("Session expired. Please login again.")
    st.session_state.token = None
    st.session_state.user = None
    cookies["token"] = ""
    cookies["username"] = ""
    cookies.save()
    st.markdown('<meta http-equiv="refresh" content="0; url=/" />', unsafe_allow_html=True)
else:
    st.error(f"❌ Failed to load data: {data.get('message', 'Error')}")
