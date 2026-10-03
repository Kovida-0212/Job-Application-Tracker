function confirmDelete() {
    return confirm("Are you sure you want to delete this application? This action cannot be undone.");
}

setTimeout(() => {
    document.querySelectorAll('.alert').forEach(alert => {
        try {
            bootstrap.Alert.getOrCreateInstance(alert).close();
        } catch (e) {}
    });
}, 4000);
