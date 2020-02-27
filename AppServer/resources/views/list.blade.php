<!DOCTYPE html>
    @forelse ($urls as $url)
        <li>{{ $url }}</li>
    @empty
        <p>No urls</p>
    @endforelse
</html>
