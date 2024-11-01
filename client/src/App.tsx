import React, { useRef, useState, useEffect } from 'react';
import { BackHandler, Alert } from 'react-native';
import { WebView } from 'react-native-webview';

const MyWebView = () => {
  const webViewRef = useRef(null);
  const [canGoBack, setCanGoBack] = useState(false);

  useEffect(() => {
    const backHandler = BackHandler.addEventListener(
      'hardwareBackPress',
      () => {
        if (canGoBack && webViewRef.current) {
          webViewRef.current.goBack();
          return true;
        } else {
          Alert.alert(
            '종료하시겠어요?',
            '앱을 종료하시겠습니까?',
            [
              { text: '취소', onPress: () => {}, style: 'cancel' },
              { text: '확인', onPress: () => BackHandler.exitApp() },
            ],
            { cancelable: false }
          );
          return true;
        }
      }
    );

    return () => backHandler.remove();
  }, [canGoBack]);

  return (
    <WebView
      ref={webViewRef}
      source={{ uri: 'http://203.252.230.246:8444/' }}
      style={{ marginTop: 0 }}
      onNavigationStateChange={(navState) => setCanGoBack(navState.canGoBack)}
    />
  );
};

export default MyWebView;
