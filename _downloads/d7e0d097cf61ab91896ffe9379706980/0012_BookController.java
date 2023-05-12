/*
 * This file is auto-generated.  DO NOT MODIFY.
 */
package com.example.aidl;
public interface BookController extends android.os.IInterface
{
  /** Default implementation for BookController. */
  public static class Default implements com.example.aidl.BookController
  {
    @Override public java.util.List<com.example.aidl.Book> getBookList() throws android.os.RemoteException
    {
      return null;
    }
    @Override public void addBookInOut(com.example.aidl.Book book) throws android.os.RemoteException
    {
    }
    @Override public void setCallBack(com.example.aidl.ICallBack callback) throws android.os.RemoteException
    {
    }
    @Override
    public android.os.IBinder asBinder() {
      return null;
    }
  }
  /** Local-side IPC implementation stub class. */
  public static abstract class Stub extends android.os.Binder implements com.example.aidl.BookController
  {
    private static final java.lang.String DESCRIPTOR = "com.example.aidl.BookController";
    /** Construct the stub at attach it to the interface. */
    public Stub()
    {
      this.attachInterface(this, DESCRIPTOR);
    }
    /**
     * Cast an IBinder object into an com.example.aidl.BookController interface,
     * generating a proxy if needed.
     */
    public static com.example.aidl.BookController asInterface(android.os.IBinder obj)
    {
      if ((obj==null)) {
        return null;
      }
      android.os.IInterface iin = obj.queryLocalInterface(DESCRIPTOR);
      if (((iin!=null)&&(iin instanceof com.example.aidl.BookController))) {
        return ((com.example.aidl.BookController)iin);
      }
      return new com.example.aidl.BookController.Stub.Proxy(obj);
    }
    @Override public android.os.IBinder asBinder()
    {
      return this;
    }
    @Override public boolean onTransact(int code, android.os.Parcel data, android.os.Parcel reply, int flags) throws android.os.RemoteException
    {
      java.lang.String descriptor = DESCRIPTOR;
      switch (code)
      {
        case INTERFACE_TRANSACTION:
        {
          reply.writeString(descriptor);
          return true;
        }
        case TRANSACTION_getBookList:
        {
          data.enforceInterface(descriptor);
          java.util.List<com.example.aidl.Book> _result = this.getBookList();
          reply.writeNoException();
          reply.writeTypedList(_result);
          return true;
        }
        case TRANSACTION_addBookInOut:
        {
          data.enforceInterface(descriptor);
          com.example.aidl.Book _arg0;
          if ((0!=data.readInt())) {
            _arg0 = com.example.aidl.Book.CREATOR.createFromParcel(data);
          }
          else {
            _arg0 = null;
          }
          this.addBookInOut(_arg0);
          reply.writeNoException();
          if ((_arg0!=null)) {
            reply.writeInt(1);
            _arg0.writeToParcel(reply, android.os.Parcelable.PARCELABLE_WRITE_RETURN_VALUE);
          }
          else {
            reply.writeInt(0);
          }
          return true;
        }
        case TRANSACTION_setCallBack:
        {
          data.enforceInterface(descriptor);
          com.example.aidl.ICallBack _arg0;
          _arg0 = com.example.aidl.ICallBack.Stub.asInterface(data.readStrongBinder());
          this.setCallBack(_arg0);
          reply.writeNoException();
          return true;
        }
        default:
        {
          return super.onTransact(code, data, reply, flags);
        }
      }
    }
    private static class Proxy implements com.example.aidl.BookController
    {
      private android.os.IBinder mRemote;
      Proxy(android.os.IBinder remote)
      {
        mRemote = remote;
      }
      @Override public android.os.IBinder asBinder()
      {
        return mRemote;
      }
      public java.lang.String getInterfaceDescriptor()
      {
        return DESCRIPTOR;
      }
      @Override public java.util.List<com.example.aidl.Book> getBookList() throws android.os.RemoteException
      {
        android.os.Parcel _data = android.os.Parcel.obtain();
        android.os.Parcel _reply = android.os.Parcel.obtain();
        java.util.List<com.example.aidl.Book> _result;
        try {
          _data.writeInterfaceToken(DESCRIPTOR);
          boolean _status = mRemote.transact(Stub.TRANSACTION_getBookList, _data, _reply, 0);
          if (!_status && getDefaultImpl() != null) {
            return getDefaultImpl().getBookList();
          }
          _reply.readException();
          _result = _reply.createTypedArrayList(com.example.aidl.Book.CREATOR);
        }
        finally {
          _reply.recycle();
          _data.recycle();
        }
        return _result;
      }
      @Override public void addBookInOut(com.example.aidl.Book book) throws android.os.RemoteException
      {
        android.os.Parcel _data = android.os.Parcel.obtain();
        android.os.Parcel _reply = android.os.Parcel.obtain();
        try {
          _data.writeInterfaceToken(DESCRIPTOR);
          if ((book!=null)) {
            _data.writeInt(1);
            book.writeToParcel(_data, 0);
          }
          else {
            _data.writeInt(0);
          }
          boolean _status = mRemote.transact(Stub.TRANSACTION_addBookInOut, _data, _reply, 0);
          if (!_status && getDefaultImpl() != null) {
            getDefaultImpl().addBookInOut(book);
            return;
          }
          _reply.readException();
          if ((0!=_reply.readInt())) {
            book.readFromParcel(_reply);
          }
        }
        finally {
          _reply.recycle();
          _data.recycle();
        }
      }
      @Override public void setCallBack(com.example.aidl.ICallBack callback) throws android.os.RemoteException
      {
        android.os.Parcel _data = android.os.Parcel.obtain();
        android.os.Parcel _reply = android.os.Parcel.obtain();
        try {
          _data.writeInterfaceToken(DESCRIPTOR);
          _data.writeStrongBinder((((callback!=null))?(callback.asBinder()):(null)));
          boolean _status = mRemote.transact(Stub.TRANSACTION_setCallBack, _data, _reply, 0);
          if (!_status && getDefaultImpl() != null) {
            getDefaultImpl().setCallBack(callback);
            return;
          }
          _reply.readException();
        }
        finally {
          _reply.recycle();
          _data.recycle();
        }
      }
      public static com.example.aidl.BookController sDefaultImpl;
    }
    static final int TRANSACTION_getBookList = (android.os.IBinder.FIRST_CALL_TRANSACTION + 0);
    static final int TRANSACTION_addBookInOut = (android.os.IBinder.FIRST_CALL_TRANSACTION + 1);
    static final int TRANSACTION_setCallBack = (android.os.IBinder.FIRST_CALL_TRANSACTION + 2);
    public static boolean setDefaultImpl(com.example.aidl.BookController impl) {
      // Only one user of this interface can use this function
      // at a time. This is a heuristic to detect if two different
      // users in the same process use this function.
      if (Stub.Proxy.sDefaultImpl != null) {
        throw new IllegalStateException("setDefaultImpl() called twice");
      }
      if (impl != null) {
        Stub.Proxy.sDefaultImpl = impl;
        return true;
      }
      return false;
    }
    public static com.example.aidl.BookController getDefaultImpl() {
      return Stub.Proxy.sDefaultImpl;
    }
  }
  public java.util.List<com.example.aidl.Book> getBookList() throws android.os.RemoteException;
  public void addBookInOut(com.example.aidl.Book book) throws android.os.RemoteException;
  public void setCallBack(com.example.aidl.ICallBack callback) throws android.os.RemoteException;
}
