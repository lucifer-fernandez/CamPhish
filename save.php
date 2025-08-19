<?php
header('Content-Type: application/json');
$data = json_decode(file_get_contents('php://input'), true);
$images = $data['images'] ?? [];
$folder = __DIR__ . '/uploads';
if (!is_dir($folder)) mkdir($folder, 0777, true);
foreach($images as $i=>$img){
    $img = str_replace('data:image/png;base64,','',$img);
    $img = str_replace(' ','+',$img);
    file_put_contents($folder.'/photo_'.time().'_'.$i.'.png', base64_decode($img));
}
echo json_encode(['status'=>'success']);
?>
